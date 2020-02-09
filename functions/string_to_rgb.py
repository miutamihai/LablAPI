import base64
from io import BytesIO
from functions.base64_normalisation import base64_normalisation

# Take in base64 string and return cv image
from PIL import Image


def stringToRGB(base64_string):
    input_bytes = bytearray(base64_string, 'utf-8')
    im = Image.open(input_bytes)
    return im
