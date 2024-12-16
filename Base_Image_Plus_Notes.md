# Title: Apply Small Images to A Base Image

## Description

A script that will take a base image "big_file" and create a new image "out_file" that has a series of given smaller files copied into it.

## Requirements

- a python script
- use the pillow module for image manipluation
- use the toml module for the config file
- use the logging module for proper logging.
- catch errors with try...except blocks
- all of the input information is stored in a toml config file.
- the toml file is refrenced at the command-line
- 

## Inputs:

big_file: a full file path
little_files: a full file glob path with a * to inditate a wildcard. sort found files in alphabetical order.
bounding_box: (Width:Height:Left:Top) the box where the little_files will be placed inside of the big_file
gap: space in pixels between each little_image (default=5)
out_file: a full file path to save the new file.

## High-Level Pseudo Code

1. get the sizes of the small files
2. calculate what size to resize the small files to give the available space of the bounding_box and the gap
3. calculate where the little files should be placed so that they are evenly spaced horizontally and centered vertially in the bounding box
4. create a copy of the big file using the given out_file path.
5. modify the new file by adding the little files.

