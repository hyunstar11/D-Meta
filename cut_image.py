import random
from PIL import Image
import argparse
import os

def random_transformations(image):
    # Randomly transform the input image by flipping, mirroring and rotating it
    mirror = random.choice([True, False])
    flip = random.choice([True, False])
    rotate = random.randint(0, 1)

    if mirror:
        image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
    if flip:
        image = image.transpose(method=Image.FLIP_TOP_BOTTOM)
    if rotate:
        image = image.transpose(method=Image.ROTATE_90)

    return image

def segment_image(image_path, m, n, prefix):
    # Load the input image and calculate the width and height of each segment
    with Image.open(image_path) as image:
        width, height = image.size
        segment_width = width // m
        segment_height = height // n
        
        # Segment the input image into m x n parts and randomly transform each segment
        for i in range(m):
            for j in range(n):
                left = i * segment_width
                top = j * segment_height
                right = (i + 1) * segment_width
                bottom = (j + 1) * segment_height
                
                segment = image.crop((left, top, right, bottom))
                transformed_segment = random_transformations(segment)
                
                # Generate a randomized output filename and save each transformed segment
                random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))
                filename = f"{prefix}_{random_string}.jpg"
                transformed_segment.save(filename)


if __name__ == "__main__":
    # Define the command-line arguments using argparse
    parser = argparse.ArgumentParser(description="Cut an image into M by N and randomly transform the partial images.")
    parser.add_argument("image_path", type=str, help="Path to the input image file.")
    parser.add_argument("m", type=int, help="Number of segments along the width of the image.")
    parser.add_argument("n", type=int, help="Number of segments along the height of the image.")
    parser.add_argument("prefix", type=str, help="Prefix for the output filenames.")
    args = parser.parse_args()

    # Call the segment_image() function with the command-line arguments
    segment_image(args.image_path, args.m, args.n, args.prefix)

