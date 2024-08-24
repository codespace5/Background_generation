import base64, requests, io, os
from tkinter.filedialog import askopenfilename
from PIL import Image, PngImagePlugin
from config import URL, NEGATIVE_PROMPT, PROMPT

# URL = f'http://38.147.83.27:40230'

def get_filepath():
    root_dir = 'remove_bg'
    return os.path.join(root_dir, 'remove_bg' + str(len(os.listdir(root_dir))) + '.png')

def _main():
    with open('1.png', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    payload ={
                "input_image": encoded_string,
                # "model": 'u2net',
            }
    response = requests.post(url=f'{URL}/v1/generation/image-to-image/remove-background', json=payload) 

    print(response.status_code)
    if response.status_code == 200:

        r = response.json()

        res_image =  r['image']
        image = Image.open(io.BytesIO(base64.b64decode(res_image.split(",",1)[0])))

        # png_payload = {
        #     "image": "data:image/png;base64," + res_image
        # }
        # response2 = requests.post(url=f'{URL}/sdapi/v1/png-info', json=png_payload)

        # pnginfo = PngImagePlugin.PngInfo()
        # pnginfo.add_text("parameters", response2.json().get("info"))

        # print('pnginfo: ', pnginfo)

        image.save(get_filepath())


if __name__ == '__main__':
    _main()