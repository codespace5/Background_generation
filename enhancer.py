import base64, requests, io, os
from tkinter.filedialog import askopenfilename
from PIL import Image, PngImagePlugin
from config import URL
# URL = f'http://64.247.206.127:40812'

def get_filepath():
    root_dir = 'enhance'
    return os.path.join(root_dir, 'enhance' + str(len(os.listdir(root_dir))) + '.png')

def _main():
    with open('2222.png', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    payload ={
                "image": encoded_string,
                # 'upscaler_1': 'R-ESRGAN 4x+',
                # 'upscaler_2': 'R-ESRGAN 4x+'
            }
    response = requests.post(url=f'{URL}/v1/generation/enhance-image', json=payload) 

    print(response.status_code)
    if response.status_code == 200:
        r = response.json()
        res_image =  r['image']
        image = Image.open(io.BytesIO(base64.b64decode(res_image.split(",",1)[0])))
        image.save(get_filepath())


if __name__ == '__main__':
    _main()