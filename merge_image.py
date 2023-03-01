import argparse
from PIL import Image
import os
import glob

def merge_image(input_filename_prefix, m, n, output_filename):
    sub_images = []
    for filename in sorted(glob.glob(f"{input_filename_prefix}*.jpg")):
        sub_image = Image.open(filename)
        sub_images.append(sub_image)

    # Check that all images have the same size
    sizes = set(im.size for im in sub_images)
    if len(sizes) > 1:
        # Resize all images to the size of the largest image
        max_size = max(im.size for im in sub_images)
        for i in range(len(sub_images)):
            if sub_images[i].size != max_size:
                sub_images[i] = sub_images[i].resize(max_size)

    # Split the sub-images into rows and columns
    rows = [sub_images[i:i+n] for i in range(0, len(sub_images), n)]

    # Concatenate the sub-images
    merged_rows = []
    for row in rows:
        row_image = Image.new('RGB', (sum(im.width for im in row), max(im.height for im in row)))
        x = 0
        for im in row:
            row_image.paste(im, (x, 0))
            x += im.width
        merged_rows.append(row_image)
    merged_image = Image.new('RGB', (max(im.width for im in merged_rows), sum(im.height for im in merged_rows)))
    y = 0
    for row_image in merged_rows:
        merged_image.paste(row_image, (0, y))
        y += row_image.height

    # Save the merged image
    merged_image.save(output_filename)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename_prefix", help="prefix of the input sub-image filenames")
    parser.add_argument("column_num", type=int, help="number of columns in the input sub-images")
    parser.add_argument("row_num", type=int, help="number of rows in the input sub-images")
    parser.add_argument("output_filename", help="filename of the merged output image")
    args = parser.parse_args()

    # Call merge_image function with command-line arguments
    merge_image(args.input_filename_prefix, args.column_num, args.row_num, args.output_filename)
