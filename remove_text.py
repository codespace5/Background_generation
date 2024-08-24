import base64, requests, io, os
from PIL import Image, PngImagePlugin
import numpy as np

from config import URL, NEGATIVE_PROMPT, PROMPT

# NEGATIVE_PROMPT = """oversaturated, ugly, render, cartoon, grain, low-res, kitsch, anime, painting, bad, disfigured
# """
# PROMPT = """Position the Alphamale supplement on a sleek, reflective obsidian platform. Behind it, a gradient backdrop transitions from a powerful deep blue at the base to a fiery orange at the top, symbolizing energy and vitality. Neon-lit graphics with bold claims hover beside the product, all illuminated by a radiant overhead spotlight that casts a dramatic shadow, encapsulating a dynamic and vibrant advertising shot.
# """
# URL = f'http://64.247.206.127:41622'

def get_filepath():
    root_dir = 'remove_text'
    return os.path.join(root_dir, 'remove_text' + str(len(os.listdir(root_dir))) + '.png')

def _main():
    
    with open('3.png', "rb") as image_file:
        image_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open('mask_bamboo.png', 'rb') as mask_file:
        mask_string = base64.b64encode(mask_file.read()).decode('utf-8')

    payload ={
        "prompt": "",
        "negative_prompt": "",
        # "seed": -1,
        # "sampler_name": "DPM++ 3M SDE Karras",
        # "steps": 60,
        # "cfg_scale": 18,
        # "width": 1024,
        # "height": 1024,
        # "denoising_strength": 0.75,
        # "refiner_checkpoint": "sd_xl_refiner_1.0_0.9vae.safetensors",
        # "refiner_switch_at": 0.8,
        "init_images": [
            image_string
        ],
        # "resize_mode": 2,
        # "image_cfg_scale": 0,
        "mask": mask_string,
        # "mask_blur": 1,
        # "inpainting_fill": 0,
        # "inpainting_mask_invert": 0,
        # "alwayson_scripts": {
        #     "controlnet": {
        #         "args": [
        #             {
        #                 # "input_image": image_string,
        #                 "module": "inpaint_only",
        #                 "model": "sd_xl_inpainting [294fe2af]",
        #                 "pixel_perfect": True,
        #                 "resize_mode": 2,
        #                 "control_mode": 1,
                        
        #             }
        #         ]
        #     }
        # }
    }

    response = requests.post(url=f'{URL}/v1/generation/inpaint-outpaint', json=payload)
    print(response.status_code)
    if response.status_code == 200:
        r = response.json()
        result = r['images'][0]
        image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
        image.save(get_filepath())
        image = np.array(image)
        return image

if __name__ == '__main__':
    _main()