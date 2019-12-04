import os

import cv2
import numpy as np
from PIL import Image


def preprocess_input(image):
    # org_image = Image.open(filename)
    # image = cv2.cvtColor(np.array(org_image), cv2.COLOR_RGB2BGR)
    if image is None:
        print('Can not read/find the image at ')
        exit(-1)

    hsv_image = cv2.cvtColor(np.float32(image), cv2.COLOR_BGR2HSV)
    H, S, V = hsv_image[:, :, 0], hsv_image[:, :, 1], hsv_image[:, :, 2]
    V = V * 2

    hsv_image = cv2.merge([H, S, V])
    image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    Dx = cv2.Sobel(image, cv2.CV_8UC1, 1, 0)
    Dy = cv2.Sobel(image, cv2.CV_8UC1, 0, 1)
    M = cv2.addWeighted(Dx, 1, Dy, 1, 0)
    ret, binary = cv2.threshold(M, 10, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    output_path = os.path.join('processed.png')
    cv2.imwrite(output_path, binary)
    return output_path
