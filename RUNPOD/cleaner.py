from fastapi import FastAPI, Body

from modules.api.models import *
from modules.api import api
import gradio as gr

from scripts import lama
from modules.shared import opts,OptionInfo
from datetime import datetime
import requests
import time, os


def cleanup_api(_: gr.Blocks, app: FastAPI):

    @app.post("/cleanup")
    def clean_up(
        input_image: str = Body("", title='cleanup input image'),
        mask: str = Body("", title='clean up mask')
    ):

        _image = api.decode_base64_to_image(input_image)
        _mask = api.decode_base64_to_image(mask)
        
        _output = lama.clean_object(_image,_mask)
        
        if len(_output) > 0:
            # print("/v1/generation/remove-text: ", "OK")

            print(time.ctime() + " /Cleaner: Object has been successfully removed.")
            current_date = datetime.today().strftime('%Y-%m-%d')
            
            if not os.path.exists(f"logs/{current_date}"):
                with open(f"logs/{current_date}", 'w') as f:
                    f.write(time.ctime() + " /Cleaner: Object has been successfully removed.\n")
            else:
                with open(f"logs/{current_date}", 'a') as f:
                    f.write(time.ctime() + " /Cleaner: Object has been successfully removed.\n")

            
            return {"code": 0, "message":"ok", "image":  api.encode_pil_to_base64(_output[0]).decode("utf-8")}
        else:
            # print("/v1/generation/remove-text: ", "Image generation failed")

            print(time.ctime() + " /Cleaner: Object Removing Failed")
            current_date = datetime.today().strftime('%Y-%m-%d')
            
            if not os.path.exists(f"logs/{current_date}"):
                with open(f"logs/{current_date}", 'w') as f:
                    f.write(time.ctime() + " /Cleaner: Object Removing Failed.\n")
            else:
                with open(f"logs/{current_date}", 'a') as f:
                    f.write(time.ctime() + " /Cleaner: Object Removing Failed.\n")

            
            return {"code": -1, "message":"Image generation failed"}


    @app.post("/v1/generation/remove-text")
    def remove_text(
        input_image: str = Body("", title='cleanup input image'),
        mask: str = Body("", title='clean up mask')
    ):

        setting = {
            "sd_model_checkpoint": "sdxl_inpainting.safetensors [df85887014]",
            "CLIP_stop_at_last_layers": 2
        }

        # api.Api.set_config(req=setting)
        URL = 'https://ufq2wdq2xnfsxx-7860.proxy.runpod.net'
        response = requests.post(url=f'{URL}/sdapi/v1/options', json=setting)
    
        print("change model for cleaner: ", response.status_code)
        
        _image = api.decode_base64_to_image(input_image)
        _mask = api.decode_base64_to_image(mask)
        
        
        _output = lama.clean_object(_image,_mask)
        
        if len(_output) > 0:
            # print("/v1/generation/remove-text: ", "OK")

            print(time.ctime() + " /v1/generation/remove-text: Text has been successfully removed.")
            current_date = datetime.today().strftime('%Y-%m-%d')
            
            if not os.path.exists(f"logs/{current_date}"):
                with open(f"logs/{current_date}", 'w') as f:
                    f.write(time.ctime() + " /v1/generation/remove-text: Text has been successfully removed.\n")
            else:
                with open(f"logs/{current_date}", 'a') as f:
                    f.write(time.ctime() + " /v1/generation/remove-text: Text has been successfully removed.\n")

            
            return {"code": 0, "message":"ok", "image":  api.encode_pil_to_base64(_output[0]).decode("utf-8")}
        else:
            # print("/v1/generation/remove-text: ", "Image generation failed")

            print(time.ctime() + " /v1/generation/remove-text: Text Removing Failed")
            current_date = datetime.today().strftime('%Y-%m-%d')
            
            if not os.path.exists(f"logs/{current_date}"):
                with open(f"logs/{current_date}", 'w') as f:
                    f.write(time.ctime() + " /v1/generation/remove-text: Text Removing Failed.\n")
            else:
                with open(f"logs/{current_date}", 'a') as f:
                    f.write(time.ctime() + " /v1/generation/remove-text: Text Removing Failed.\n")

            
            return {"code": -1, "message":"Image generation failed"}


try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(cleanup_api)
except:
    pass
