import sys
import glob
import toml
from PIL import Image
from log import setup_logging
from args import get_options


args = get_options()
log = setup_logging(log_to_console=True)


def load_config():
    """
    Load configuration from a TOML file.
    """

    config = {}
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = toml.load(f)
        except FileNotFoundError:
            log.error(f"Config file not found: {args.config}")
            sys.exit(1)
        except toml.TomlDecodeError as e:
            log.error(f"Error parsing TOML file: {e}")
            sys.exit(1)

    if args.big_file:
        config['big_file'] = args.big_file

    if args.little_files:
        config['little_files'] = args.little_files

    if args.output_file:
        config['out_file'] = args.output_file
        
    if args.gap != config.get('gap') and args.gap != 10:
        config['gap'] = args.gap

    if args.box:
        x, y, w, h = map(int, args.box.split(','))
        config['bounding_box']['width'] = w
        config['bounding_box']['height'] = h
        config['bounding_box']['left'] = x
        config['bounding_box']['top'] = y


    if args.gap:
        config['gap'] = args.gap

    return config

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
            log.warning(f"No files found matching pattern: {little_files_pattern}")
        return little_files
    except Exception as e:
        log.error(f"Error finding little files: {e}")
        return []

def calculate_little_image_sizes(little_files, bounding_box, gap):
    """
    Calculate sizes for little images while maintaining aspect ratio.
    
    Args:
        little_files (list): List of little image paths
        bounding_box (dict): Bounding box specifications
        gap (int): Gap between images
    
    Returns:
        list: List of (width, height) tuples for resizing little images
    """
    # Unpack bounding box
    box_width = bounding_box['width']
    box_height = bounding_box['height']
    
    # Calculate how many images can fit horizontally
    num_images = len(little_files)
    total_gap_width = (num_images - 1) * gap
    
    # Calculate available width for images
    available_width = box_width - total_gap_width
    
    # Initialize list to store image sizes
    image_sizes = []
    
    # Calculate size for each image maintaining its aspect ratio
    for little_file in little_files:
        # Open original image to get its aspect ratio
        with Image.open(little_file) as img:
            orig_width, orig_height = img.size
        
        # Calculate width based on even distribution
        image_width = available_width // num_images
        
        # Calculate height maintaining original aspect ratio
        image_height = int(image_width * (orig_height / orig_width))
        
        # Ensure height doesn't exceed bounding box height
        if image_height > box_height:
            image_height = box_height
            image_width = int(image_height * (orig_width / orig_height))
        
        image_sizes.append((image_width, image_height))
    
    return image_sizes

def place_little_images(big_image, little_files, image_sizes, bounding_box, gap):
    """
    Place little images onto the big image.
    
    Args:
        big_image (Image): Base image to modify
        little_files (list): List of little image paths
        image_sizes (list): List of (width, height) for little images
        bounding_box (dict): Bounding box specifications
        gap (int): Gap between images
    
    Returns:
        Image: Modified big image with little images placed
    """
    try:
        # Unpack bounding box
        
        box_left = int(bounding_box['left'])
        box_top = int(bounding_box['top'])
        box_height = int(bounding_box['height'])
        
        # Calculate vertical centering
        vertical_center = box_top + (box_height // 2)
        
        # Create a new image for compositing
        big_image_with_transparency = big_image.convert("RGBA")
        
        for idx, (little_file, (width, height)) in enumerate(zip(little_files, image_sizes)):
            little_img = Image.open(little_file).convert("RGBA")  # Ensure image is in RGBA mode
            little_img_resized = little_img.resize((width, height), Image.LANCZOS)
            
            # Calculate x position
            x_pos = box_left + (idx * (width + gap))
            
            # Calculate y position (centered vertically)
            y_pos = vertical_center - (height // 2)
            
            # Create a mask for the little image
            mask = Image.new("RGBA", big_image_with_transparency.size)
            mask.paste(little_img_resized, (x_pos, y_pos))
            
            # Paste the little image using alpha_composite
            big_image_with_transparency = Image.alpha_composite(big_image_with_transparency, mask)
        
        return big_image_with_transparency
    except Exception as e:
        log.error(f"Error placing little images: {e}")
        raise

def main():
    """
    Main function to process images based on configuration.
    
    Args:
        config_path (str): Path to the configuration TOML file
    """
    
    try:
        # Load configuration
        config = load_config()
        # log.info(f"Config: {config}")
        # log.info(f"gap: {config.get('gap', 5)}")
        
        # Find and sort little files
        little_files = find_and_sort_little_files(config.get('little_files', ''))
        
        # Open big image
        big_image = Image.open(config.get('big_file', '')).copy()
        
        # Calculate little image size
        little_image_size = calculate_little_image_sizes(
            little_files, 
            config.get('bounding_box', {}), 
            config.get('gap', 5)
        )

        # Place little images
        modified_image = place_little_images(
            big_image = big_image, 
            little_files = little_files, 
            image_sizes = little_image_size, 
            bounding_box = config['bounding_box'], 
            gap = config.get('gap', 5)
        )
        
        # Save output image
        modified_image.save(config['out_file'])
        log.info(f"Image successfully processed. Output saved to {config['out_file']}")
    
    except Exception as e:
        log.error(f"Error occurred :: Config :: {config}")
        log.error(f"Error occurred :: Type: {type(e).__name__} :: Message: {str(e)}", exc_info=sys.exc_info())
        sys.exit(1)

if __name__ == "__main__":
    
    main()