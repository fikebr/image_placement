import os
import sys
import glob
import logging
import toml
from PIL import Image
# Usage:
import logging
from log import setup_logging
setup_logging()
# logging.error("This is an error message")



# def setup_logging():
#     """Configure logging for the application."""
#     LOG_FORMAT = "%(asctime)s %(levelname)s %(lineno)d - %(message)s"  # %(filename)s
#     DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
#     LOG_FILE = "logs/app.log"
#     LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10 MB




#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(levelname)s: %(message)s',
#         datefmt='%Y-%m-%d %H:%M:%S'
#     )
#     return logging.getLogger(__name__)

def load_config(config_path):
    """
    Load configuration from a TOML file.
    
    Args:
        config_path (str): Path to the TOML configuration file
    
    Returns:
        dict: Parsed configuration
    """
    try:
        with open(config_path, 'r') as f:
            return toml.load(f)
    except FileNotFoundError:
        logging.error(f"Config file not found: {config_path}")
        sys.exit(1)
    except toml.TomlDecodeError as e:
        logging.error(f"Error parsing TOML file: {e}")
        sys.exit(1)

def find_and_sort_little_files(little_files_pattern):
    """
    Find and sort little files based on the given glob pattern.
    
    Args:
        little_files_pattern (str): Glob pattern to find image files
    
    Returns:
        list: Sorted list of little file paths
    """
    try:
        little_files = sorted(glob.glob(little_files_pattern))
        if not little_files:
            logging.warning(f"No files found matching pattern: {little_files_pattern}")
        return little_files
    except Exception as e:
        logging.error(f"Error finding little files: {e}")
        return []

def calculate_little_image_size(big_image, little_files, bounding_box, gap):
    """
    Calculate the size to resize little images to fit in the bounding box.
    
    Args:
        big_image (Image): Base image
        little_files (list): List of little image paths
        bounding_box (dict): Bounding box specifications
        gap (int): Gap between images
    
    Returns:
        tuple: (width, height) for resizing little images
    """
    # Unpack bounding box
    box_width = bounding_box['width']
    box_height = bounding_box['height']
    
    # Calculate how many images can fit horizontally
    num_images = len(little_files)
    total_gap_width = (num_images - 1) * gap
    
    # Calculate available width for images
    available_width = box_width - total_gap_width
    image_width = available_width // num_images
    
    # Calculate height maintaining aspect ratio
    image_height = int(image_width * (box_height / box_width))
    
    return (image_width, image_height)

def place_little_images(big_image, little_files, bounding_box, little_image_size, gap):
    """
    Place little images onto the big image.
    
    Args:
        big_image (Image): Base image to modify
        little_files (list): List of little image paths
        bounding_box (dict): Bounding box specifications
        little_image_size (tuple): Size to resize little images
        gap (int): Gap between images
    
    Returns:
        Image: Modified big image with little images placed
    """
    try:
        # Unpack bounding box
        box_left = bounding_box['left']
        box_top = bounding_box['top']
        box_height = bounding_box['height']
        
        # Calculate vertical centering
        vertical_center = box_top + (box_height // 2)
        
        for idx, little_file in enumerate(little_files):
            little_img = Image.open(little_file)
            little_img_resized = little_img.resize(little_image_size)
            
            # Calculate x position
            x_pos = box_left + (idx * (little_image_size[0] + gap))
            
            # Calculate y position (centered vertically)
            y_pos = vertical_center - (little_image_size[1] // 2)
            
            # Paste the little image
            big_image.paste(little_img_resized, (x_pos, y_pos))
        
        return big_image
    except Exception as e:
        logging.error(f"Error placing little images: {e}")
        raise

def main(config_path):
    """
    Main function to process images based on configuration.
    
    Args:
        config_path (str): Path to the configuration TOML file
    """
    setup_logging()
    
    try:
        # Load configuration
        config = load_config(config_path)
        
        logging.info(f"Configuration loaded from {config_path}")
        logging.debug(f"Configuration: {config}")
        
        # Find and sort little files
        little_files = find_and_sort_little_files(config['little_files'])
        
        # Open big image
        big_image = Image.open(config['big_file']).copy()
        
        # Calculate little image size
        little_image_size = calculate_little_image_size(
            big_image, 
            little_files, 
            config['bounding_box'], 
            config.get('gap', 5)
        )
        
        # Place little images
        modified_image = place_little_images(
            big_image, 
            little_files, 
            config['bounding_box'], 
            little_image_size, 
            config.get('gap', 5)
        )
        
        # Save output image
        modified_image.save(config['out_file'])
        logging.info(f"Image successfully processed. Output saved to {config['out_file']}")
    
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <config_path>")
        sys.exit(1)
    
    main(sys.argv[1])