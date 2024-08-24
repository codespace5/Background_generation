import base64
import io
import json

import requests
from PIL import Image, PngImagePlugin

URL = f'http://60.33.119.199:50485'

def _main():
    payload =  {
    "prompt": "apple",
    "restore_faces": True,
    "negative_prompt": "",
    "seed": -1,
    "override_settings": {
      "sd_model_checkpoint": "sd_xl_base_1.0.safetensors",
      "sd_vae": "sdxl_vae.safetensors"
    },
    "width": 1024,
    "height": 1024,
    "guidance_scale": 7.5,
    "cfg_scale": 7,
    # "sampler_index": "Eular a",
    "steps": 60,
    "email": 'test@example.com'
  }
    # url = f'{URL}/v1/generation/text-to-image'
    # print(url)
    
    response = requests.post(url=f'{URL}/sdapi/v1/txt2img', json=payload)
    

    print(response.status_code)
    if response.status_code == 200:

        
        r = response.json()

        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

            png_payload = {
                "image": "data:image/png;base64," + i
            }
            response2 = requests.post(url=f'{URL}/sdapi/v1/png-info', json=png_payload)

            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            image.save('txt2img.png', pnginfo=pnginfo)

if __name__ == '__main__':
    _main()