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
args = parser.parse_args()

original_img = Image.open(args.input_file)
original_width, original_height = original_img.size

img_bw_quantized = original_img.convert("L").quantize(colors=args.colors)

scaling_factor = args.output_width / original_width
processed_img = img_bw_quantized.resize((args.output_width, int(scaling_factor * original_height * char_aspect)))

img_array = np.array(processed_img)

gradient = " .:-=+*#%@"
usable_gradient = [int(round(i)) for i in np.linspace(0, len(gradient) - 1, args.colors)]

with open(args.output_file, "w") as f:
    for row in img_array:
        output = ""
        for value in row:
            output += gradient[usable_gradient[value]]
        f.write(output + "\n")


