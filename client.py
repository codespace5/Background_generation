import base64
import io
import os

import cv2
import numpy as np
import requests
from PIL import Image

from config import NEGATIVE_PROMPT, PROMPT, URL


# URL = f'https://5xys6vf7v82qt4-7860.proxy.runpod.net'
# URL = f'https://100.64.0.22:56840'
# NEGATIVE_PROMPT = """oversaturated, ugly, render, cartoon, grain, low-res, kitsch, anime, painting, bad, disfigured
# """
# PROMPT = """a professional photo of a bottle and a box of pills at a tropical beach with a blue sea, award winning photography, beautiful, realistic, extremely detailed, ultra quality"""
# PROMPT = """ a professional photo of a skincare product sitting on a pedestal overgrown by green moss. Behind it in the background is a tropical rainforest, award-winning photography, cinematic lightning, 4k, photorealistic, studio quality, product photography, epic advertising style.
# """
def get_filepath():
    root_dir = 'result'
    return os.path.join(root_dir, 'result' + str(len(os.listdir(root_dir))) + '.png')

def get_base64_from_image(file_name):
    with open(file_name, "rb") as image_file:
        image_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    return image_string

def inpimg2img_with_controlnet(image_string, prompt=PROMPT, ng_prompt=NEGATIVE_PROMPT):
    payload = {
        "prompt": PROMPT,
        "negative_prompt": NEGATIVE_PROMPT,
        "batch_size": 1,
        "cfg_scale": 18,
        "steps": 70,
        "width": 1024,
        "height": 768,
        "init_images": [
            image_string
        ],
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "weight": 1,
                        "control_mode": 2,
                    }
                ]
            }
        }
    }
    response = requests.post(url=f'{URL}/v1/generation/magic-remove', json=payload, timeout=600)
    
    print(response.status_code)
    images = []
    if response.status_code == 200:
        r = response.json()
        for result in r['images']:
        # result = r['images'][1]
            image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
            images.append(np.array(image))
        return images


def magic_remove(image_array, prompt=PROMPT, ng_prompt=NEGATIVE_PROMPT):
    print("tste")
    cv2.imwrite('tmp.png', image_array)
    image_string = get_base64_from_image('tmp.png')
    os.remove('tmp.png')
    images = inpimg2img_with_controlnet(image_string=image_string, prompt=prompt, ng_prompt=ng_prompt)
    print("seefsefsef", images)
    return images
    
def _main():
    # image_array = cv2.imread('jpeg/IMG_0534.JPEG')
    image_array = cv2.imread('jpeg/1.jpg')
    images = magic_remove(image_array = image_array)
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow('image', image)
        
        cv2.imwrite(get_filepath(), image)
        cv2.waitKey(0)

if __name__ == "__main__":
    _main()
