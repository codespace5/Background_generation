import base64
import io
import time

import cv2
import numpy as np
import requests
from PIL import Image

from config import URL, get_filepath


def remove_text():
    # with open('origin_image.png', "rb") as image_file:
    with open('cars/5.JPG', "rb") as image_file:
        image_string = base64.b64encode(image_file.read()).decode('utf-8')

    image = cv2.imread('canvas_image (1).png')
    # cv2.imshow('last', image)
    image = cv2.morphologyEx(image, cv2.MORPH_DILATE, kernel=np.ones((23, 23), np.uint8))
    # cv2.imshow('la1st', image)
    # cv2.waitKey(0)
    cv2.imwrite('canvas_image.png', image)
    with open('canvas_image.png', 'rb') as mask_file:
        mask_string = base64.b64encode(mask_file.read()).decode('utf-8')

    payload = {
        "input_image": image_string,
        "mask": mask_string
    }

    response = requests.post(url=f"{URL}/v1/generation/remove-text", json=payload)

    print("image ", response.status_code)
    if response.status_code == 200:
        r = response.json()
        image = r["image"]
        image = Image.open(io.BytesIO(base64.b64decode(image.split(",",1)[0])))
        image.save(get_filepath(root_dir='remove_text'))
        image = np.array(image)
        cv2.imshow("result", image)
        cv2.waitKey(0)
        return image
    return

def _main():
    remove_text()

if __name__ == "__main__":
    _main()