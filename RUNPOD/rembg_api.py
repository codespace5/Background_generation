
from fastapi import FastAPI, Body

from modules.api.models import *
from modules.api import api
from modules.img2img import img2img
import gradio as gr
# from new_txt2img import control_sd
import rembg, cv2
import numpy as np
from PIL import Image

# models = [
#     "None",
#     "u2net",
#     "u2netp",
#     "u2net_human_seg",
#     "u2net_cloth_seg",
#     "silueta",
# ]


def rembg_api(_: gr.Blocks, app: FastAPI):
    @app.post("/v1/generation/image-to-image/remove-background")
    async def remove_bg(
        input_image: str = Body("", title='rembg input image'),
        model: str = Body("u2net", title='rembg model'), 
        return_mask: bool = Body(False, title='return mask'), 
        alpha_matting: bool = Body(False, title='alpha matting'), 
        alpha_matting_foreground_threshold: int = Body(240, title='alpha matting foreground threshold'), 
        alpha_matting_background_threshold: int = Body(10, title='alpha matting background threshold'), 
        alpha_matting_erode_size: int = Body(10, title='alpha matting erode size')
    ):
        model = 'u2net'
        if not model or model == "None":
            return

        input_image = api.decode_base64_to_image(input_image)

        image = rembg.remove(
            input_image,
            session=rembg.new_session(model),
            only_mask=False,
            alpha_matting=False,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
            alpha_matting_erode_size=10,
        )

        return {"image": api.encode_pil_to_base64(image).decode("utf-8")}
    
    @app.post("/v1/generation/image-to-image/masking")
    async def get_mask(
        input_image: str = Body("", title='rembg input image'),
        model: str = Body("u2net", title='rembg model'), 
        
        return_mask: bool = Body(True, title='return mask'), 
        alpha_matting: bool = Body(False, title='alpha matting'), 
        alpha_matting_foreground_threshold: int = Body(240, title='alpha matting foreground threshold'), 
        alpha_matting_background_threshold: int = Body(10, title='alpha matting background threshold'), 
        alpha_matting_erode_size: int = Body(10, title='alpha matting erode size')
    ):
        model = 'u2net'
        if not model or model == "None":
            return

        input_image = api.decode_base64_to_image(input_image)

        image = rembg.remove(
            input_image,
            session=rembg.new_session(model),
            only_mask=True,
            alpha_matting=False,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
            alpha_matting_erode_size=10,
        )

        return {"image": api.encode_pil_to_base64(image).decode("utf-8")}


    # @app.post("/magic-remove")
    # async def magic_remove(
    #     input_image: str = Body("", title='rembg input image'),
    #     model: str = Body("u2net", title='rembg model'), 
    #     alpha_matting: bool = Body(False, title='alpha matting'), 
    #     alpha_matting_foreground_threshold: int = Body(240, title='alpha matting foreground threshold'), 
    #     alpha_matting_background_threshold: int = Body(10, title='alpha matting background threshold'), 
    #     alpha_matting_erode_size: int = Body(10, title='alpha matting erode size'),
    #     # id_task: str = Body('task(fiytnho7t8iayt5)', title='id_task'),
    #     # mode: int = Body(4, title='id_task'),
    #     prompt: str = Body('', title='prompt'),
    #     negative_prompt: str = Body('', title='negative_prompt'),


    # ):
    #     if not model or model == "None":
    #         return

    #     input_image = api.decode_base64_to_image(input_image)

    #     masked_image = rembg.remove(
    #         input_image,
    #         session=rembg.new_session(model),
    #         only_mask=True,
    #         alpha_matting=alpha_matting,
    #         alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
    #         alpha_matting_background_threshold=alpha_matting_background_threshold,
    #         alpha_matting_erode_size=alpha_matting_erode_size,
    #     )

    #     object_image = rembg.remove(
    #         input_image,
    #         session=rembg.new_session(model),
    #         only_mask=False,
    #         alpha_matting=alpha_matting,
    #         alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
    #         alpha_matting_background_threshold=alpha_matting_background_threshold,
    #         alpha_matting_erode_size=alpha_matting_erode_size,
    #     )

    #     image = control_sd(img=object_image, url=f'127.0.0.1:7860/sdapi/v1/txt2img', prompt=prompt, negative_prompt=negative_prompt)
    #     image = np.array(image)
    #     masked_image = np.array(masked_image)
    #     object_image = np.array(object_image)

    #     mask_image = cv2.resize(mask_image, (1024, 1024))
    #     object_image = cv2.resize(object_image, (1024, 1024))
    #     image = cv2.resize(image, (1024, 1027))

    #     mask_image = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
    #     _, mask_image = cv2.threshold(mask_image, 127, 255, cv2.THRESH_BINARY)
    #     mask_image = cv2.cvtColor(mask_image, cv2.COLOR_GRAY2BGR)

        

    #     # mask1_image = cv2.dilate(mask_image, np.ones((2, 1), np.uint8))
    #     cutted_image = cv2.bitwise_and(object_image, mask_image)

    #     reverse_mask = 255 - mask_image
    #     background_image = cv2.bitwise_and(image, reverse_mask)

    #     result_image = cv2.bitwise_or(cutted_image, background_image)
    #     im = Image.fromarray(np.uint8(result_image))


        # prompt_styles = [] 
        # init_img = None 
        # sketch = None 
        # init_img_with_mask = None 
        # inpaint_color_sketch = None 
        # inpaint_color_sketch_orig = None 
        # init_img_inpaint = object_image
        # init_mask_inpaint = masked_image
        # img2img_batch_input_dir = ''
        # img2img_batch_output_dir = ''
        # img2img_batch_inpaint_mask_dir = ''
        # override_settings_texts = [] 
        # img2img_batch_use_png_info = False 
        # img2img_batch_png_info_props = [] 
        # img2img_batch_png_info_dir = ''
        # args = (0, False, '', 0.8, 454545453453, False, -1, 0, 0, 0, '<scripts.controlnet_ui.controlnet_ui_group.UiControlNetUnit object at 0x7fa9844dd2d0>', '* `CFG Scale` should be 2 or lower.', True, True, '', '', True, 50, True, 1, 0, False, 4, 0.5, 'Linear', 'None', '<p style="margin-bottom:0.75em">Recommended settings: Sampling Steps: 80-100, Sampler: Euler a, Denoising strength: 0.8</p>', 128, 8, ['left', 'right', 'up', 'down'], 1, 0.05, 128, 4, 0, ['left', 'right', 'up', 'down'], False, False, 'positive', 'comma', 0, False, False, '', '<p style="margin-bottom:0.75em">Will upscale the image by the selected scale factor; use width and height sliders to set tile size</p>', 64, 0, 2, 1, '', [], 0, '', [], 0, '', [], True, False, False, False, 0, False, None, None, False, 50)



        # image = img2img(
        #     id_task = id_task,
        #     mode = mode ,
        #     prompt = prompt,
        #     negative_prompt = negative_prompt,
        #     prompt_styles = prompt_styles ,
        #     init_img = init_img ,
        #     sketch = sketch ,
        #     init_img_with_mask = init_img_with_mask ,
        #     inpaint_color_sketch = inpaint_color_sketch ,
        #     inpaint_color_sketch_orig = inpaint_color_sketch_orig ,
        #     init_img_inpaint = object_image,
        #     init_mask_inpaint = masked_image,
        #     steps = steps ,
        #     sampler_name =sampler_name,
        #     mask_blur = mask_blur ,
        #     mask_alpha = mask_alpha ,
        #     inpainting_fill = inpainting_fill ,
        #     batch_size = batch_size ,
        #     cfg_scale = cfg_scale ,
        #     image_cfg_scale = image_cfg_scale ,
        #     denoising_strength = denoising_strength ,
        #     selected_scale_tab = selected_scale_tab ,
        #     height = height ,
        #     width = width ,
        #     scale_by = scale_by ,
        #     resize_mode = resize_mode ,
        #     inpaint_full_res = inpaint_full_res ,
        #     inpaint_full_res_padding = inpaint_full_res_padding ,
        #     inpainting_mask_invert = inpainting_mask_invert ,
        #     img2img_batch_input_dir = img2img_batch_input_dir,
        #     img2img_batch_output_dir = img2img_batch_output_dir,
        #     img2img_batch_inpaint_mask_dir = img2img_batch_inpaint_mask_dir,
        #     override_settings_texts = override_settings_texts ,
        #     img2img_batch_use_png_info = img2img_batch_use_png_info ,
        #     img2img_batch_png_info_props = img2img_batch_png_info_props ,
        #     img2img_batch_png_info_dir = img2img_batch_png_info_dir,
        #     n_iter = 1,
        #     request = 'request',
        # )[0][0]




        return {"image": api.encode_pil_to_base64(im).decode("utf-8")}

try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(rembg_api)
except:
    pass