import requests
import argparse
import numpy as np
from PIL import Image

# usage: python img/surprised_pikachu.jpg 10 120 img/surprised_pikachu.txt

char_aspect = .6

# parsing command line inputs
parser = argparse.ArgumentParser(description="Convert an image to text")
parser.add_argument("input_file", type=str, help="path to original image")
parser.add_argument("colors", type=int, help="number of grayscale values to use on output")
parser.add_argument("output_width", type=int, help="width of output in characters")
parser.add_argument("output_file", type=str, help="path to write text file")
parser.add_argument("-w", "--web", action="store_true", help="use URL for input_file")
args = parser.parse_args()

# Handling http request for input_file if -w flag is present
if args.web:
    original_img = Image.open(requests.get(args.input_file, stream=True).raw)
else:
    original_img = Image.open(args.input_file)

# Image processing:
# Get dimensions
original_width, original_height = original_img.size
# Convert to grayscale -> reduce color palette
img_bw_quantized = original_img.convert("L").quantize(colors=args.colors)
# Rescale to account for distortion of pixels from squares -> rectangles
scaling_factor = args.output_width / original_width
processed_img = img_bw_quantized.resize((args.output_width, int(scaling_factor * original_height * char_aspect)))
# Convert to numpy array
img_array = np.array(processed_img)

# Set characters for gradient ramp / ensure that color space spans whole gradient
gradient = " .:-=+*#%@"
usable_gradient = [int(round(i)) for i in np.linspace(0, len(gradient) - 1, args.colors)]

# Write to file
with open(args.output_file, "w") as f:
    for row in img_array:
        output = ""
        for value in row:
            output += gradient[usable_gradient[value]]
        f.write(output + "\n")


