# Image Placement

This script is used to place little images onto a big image.

## Usage

```bash
usage: image_placement.py [-h] [-b BIG_FILE] [-l LITTLE_FILES] [-o OUTPUT_FILE] [-g GAP] [-c CONFIG] [-x BOX]

Image Placement - A tool to place small images in a grid on a larger image

options:
  -h, --help            show this help message and exit
  -b BIG_FILE, --big_file BIG_FILE
                        The path to the big image file
  -l LITTLE_FILES, --little_files LITTLE_FILES
                        The path to the little image files (glob pattern)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        The path to the output file
  -g GAP, --gap GAP     The gap between the little images
  -c CONFIG, --config CONFIG
                        The path to the config file (toml)
  -x BOX, --box BOX     The bounding box (x,y,w,h)
  
```

## Config TOML

The config.toml can be used to specify any of the configuration settings
If any settings in the config.toml conflict with command-line arguments the command-line will take precedence.

```markdown

# Sample configuration for image placement script

# Path to the base (big) image
big_file = "test\\river_mountains.png"

# Glob pattern for small images
little_files = "test\\small\\*.png"

# Optional: gap between images (default is 5 if not specified)
gap = 10

# Output file path
out_file = "test\\river_mountains_out.png"


# Bounding box for placing small images (Width:Height:Left:Top)
[bounding_box]
width = 776
height = 340
left = 60
top = 60

```