import argparse
import os

# https://docs.python.org/3/library/argparse.html

# USAGE
# from argparse import get_options
# args = get_options()
# print(args.rebuild)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Image Placement - A tool to place small images in a grid on a larger image'
    )

    # Add arguments
    parser.add_argument(
        '-b',
        '--big_file',
        type=str,
        help='The path to the big image file'
    )

    parser.add_argument(
        '-l',
        '--little_files',
        type=str,
        help='The path to the little image files (glob pattern)'
    )
    
    parser.add_argument(
        '-o',
        '--output_file',
        type=str,
        help='The path to the output file'
    )
    
    parser.add_argument(
        '-g',
        '--gap',
        default=10,
        type=int,
        help='The gap between the little images'
    )
    
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        help='The path to the config file (toml)'
    )
    
    parser.add_argument(
        '-x',
        '--box',
        type=str,
        help='The bounding box (x,y,w,h)'
    )


    args = parser.parse_args()
    return args

def validate_args(args):
    """Validate the parsed arguments and set defaults if needed."""
    
    if args.big_file and not os.path.exists(args.big_file):
        raise FileNotFoundError(f"Big file not found: {args.big_file}")
    
    if args.output_file and os.path.exists(args.output_file):
        raise FileExistsError(f"Output file already exists: {args.output_file}")
    
    if args.config and not os.path.exists(args.config):
        raise FileNotFoundError(f"Config file not found: {args.config}")
    
    if args.box:
        try:
            x, y, w, h = map(int, args.box.split(','))
        except ValueError:
            raise ValueError(f"Invalid bounding box: {args.box}")
        
    if not any([args.big_file, args.little_files, args.output_file, args.config, args.box]):
        raise ValueError("No arguments provided")
        
    
    return args

def get_options():
    """Get and validate command line options."""
    args = parse_args()
    return validate_args(args) 