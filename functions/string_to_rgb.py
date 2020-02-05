import base64
from io import BytesIO
from functions.base64_normalisation import base64_normalisation

# Take in base64 string and return cv image
from PIL import Image


def stringToRGB(base64_string):
    #im = Image.open(BytesIO(base64.b64decode(base64_string, '-_')))
    im = Image.open(BytesIO(base64.decodebytes(base64_string)))
    return im
