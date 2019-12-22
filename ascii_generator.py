__credits__ = ["https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/",
               "https://gist.github.com/Ronald-TR/1bb452206b97b470a2b74942de984acf"]

from PIL import Image
import os
from pprint import pprint

ASCII_CHARS = ['X', 'X', 'X', 'X', '.']


def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image


def convert_to_grayscale(image):
    return image.convert('L')


def map_pixels_to_ascii_chars(image, range_width=60):
    """Maps each pixel to an ascii char based on the range
    in which it lies.
    8-bit so 0-255 is divided into 5 ranges of 51 pixels each.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)]
                       for pixel_value in pixels_in_image]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(image, new_width=100):
    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width]
                   for index in range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)


def handle_image_conversion(image_filepath):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print("Unable to open image file {image_filepath}.".format(
            image_filepath=image_filepath))
        print(e)
        return
    image_ascii = convert_image_to_ascii(image)
    image_ascii = image_ascii.split("\n")
    image_ascii = smooth(image_ascii)
    for line in image_ascii:
        line=(line.replace(".", " "))
        line=(line.replace("X"," "))
        print(line)


def smooth(image_ascii):
    for line_index, line in enumerate(image_ascii):
        for symbol_index, symbol in enumerate(line):
            if line_index != 0 and line_index != len(image_ascii)-1 and symbol != "." and symbol_index != 0 and symbol_index != len(line)-1 and not (image_ascii[line_index-1][symbol_index] != "." and image_ascii[line_index+1][symbol_index] != "." and image_ascii[line_index+1][symbol_index+1] != "." and image_ascii[line_index+1][symbol_index-1] != "." and image_ascii[line_index-1][symbol_index+1] != "." and image_ascii[line_index-1][symbol_index-1] != "." and image_ascii[line_index][symbol_index+1] != "." and image_ascii[line_index][symbol_index-1] != "."):
                if image_ascii[line_index-1][symbol_index] != ".":
                    image_ascii[line_index] = image_ascii[line_index][:symbol_index] + \
                        "|" + image_ascii[line_index][symbol_index + 1:]
                elif image_ascii[line_index-1][symbol_index-1] != ".":
                    image_ascii[line_index] = image_ascii[line_index][:symbol_index] + \
                        "\\" + image_ascii[line_index][symbol_index + 1:]
                elif image_ascii[line_index-1][symbol_index+1] != ".":
                    image_ascii[line_index] = image_ascii[line_index][:symbol_index] + \
                        "/" + image_ascii[line_index][symbol_index + 1:]
                elif image_ascii[line_index+1][symbol_index] != ".":
                    image_ascii[line_index] = image_ascii[line_index][:symbol_index] + \
                        "|" + image_ascii[line_index][symbol_index + 1:]
                elif image_ascii[line_index+1][symbol_index-1] != ".":
                    image_ascii[line_index] = image_ascii[line_index][:symbol_index] + \
                        "/" + image_ascii[line_index][symbol_index + 1:]
                elif image_ascii[line_index+1][symbol_index+1] != ".":
                    image_ascii[line_index] = image_ascii[line_index][:symbol_index] + \
                        "\\" + image_ascii[line_index][symbol_index + 1:]
                elif image_ascii[line_index][symbol_index+1] != ".":
                    image_ascii[line_index] = image_ascii[line_index][:symbol_index] + \
                        "_" + image_ascii[line_index][symbol_index + 1:]
                elif image_ascii[line_index][symbol_index-1] != ".":
                    image_ascii[line_index] = image_ascii[line_index][:symbol_index] + \
                        "_" + image_ascii[line_index][symbol_index + 1:]
    return image_ascii


if __name__ == '__main__':
    import sys

    image = input(
        f"Choose file from {[file for file in os.listdir('images')]}\n")
    image_file_path = str(f"images/{image}")
    handle_image_conversion(image_file_path)
