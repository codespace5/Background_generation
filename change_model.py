from config import URL
import requests

def change_model(flag):
    if flag == "sdxl_base":
        option_payload = {
            "sd_model_checkpoint": "sd_xl_base_1.0_0.9vae.safetensors [e6bb9ea85b]",
            "CLIP_stop_at_last_layers": 2
        }

    if flag == "sdxl_inpainting":
        option_payload = {
            "sd_model_checkpoint": "sdxl_inpainting.safetensors [df85887014]",
            "CLIP_stop_at_last_layers": 2
        }

    response = requests.post(url=f'{URL}/sdapi/v1/options', json=option_payload)
    print("change model: ", response.status_code)
    if response.status_code == 200: 
        # print("Model has changed to sdxl_inpainting.safetensors [df85887014]")
        return flag
    else:
        return "None"
    

def _main():
    # result = change_model(flag = "sdxl_base")
    result = change_model(flag = "sdxl_inpainting")

    print(f"Model has been changed to {result}")

if __name__ == "__main__":
    _main()