import base64, requests, io, os, cv2
from tkinter.filedialog import askopenfilename
from PIL import Image, PngImagePlugin
import numpy as np
from config import URL, NEGATIVE_PROMPT, PROMPT


def get_filepath(root_dir):
    # root_dir = 'upscale'
    return os.path.join(root_dir, 'upscale' + str(len(os.listdir(root_dir))) + '.png')

def _main():
    with open('111.png', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    payload ={
            "resize_mode": 1,
            "image": encoded_string,
        }
    response = requests.post(url=f'{URL}/v1/generation/upscale-image', json=payload) 

    print(response.status_code)
    if response.status_code == 200:
        r = response.json()
        res_image =  r['image']
        image = Image.open(io.BytesIO(base64.b64decode(res_image.split(",",1)[0])))
        image.save(get_filepath(root_dir='upscale'))
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow("result", image)
        cv2.waitKey(0)
        return image


if __name__ == '__main__':
    _main()
