import os

# URL = f'https://ufq2wdq2xnfsxx-7860.proxy.runpod.net'
URL = f'https://ba3f5380794b1a37e0.gradio.live'

#NEGATIVE_PROMPT = """oversaturated, ugly, render, cartoon, grain, low-res, kitsch, anime, painting, bad, disfigured"""
#PROMPT = """a professional photo of a bottle and a box of pills at a tropical beach with a blue sea, award winning photography, beautiful, ultra detailed, ultra quality"""

NEGATIVE_PROMPT = """oversaturated, ugly, render, cartoon, grain, low-res, kitsch, anime, painting, bad, disfigured
"""
# PROMPT = """ Full of confidence with the background is inhouse,beautiful, ultra detailed, ultra quality,blond hair"""

# PROMPT = """Elevate Your Entertainment Experience with Seamless Performance and Crystal Clear Audio! Discover unparalleled stability, expansive compatibility, and effortless control. Revolutionize your media consumption with the ultimate fusion of innovation and reliability.s"""
PROMPT = """Amazon rainforest on the flat Rock in the sunny day in a shopping mall on the desk, In the shopping mall, Unleash the Power of Entertainment with the Stable Diffusion XL Base Model Media Player  in the Shopping Mall! Immerse yourself in a world of unparalleled audiovisual excellence. With seamless streaming, effortless navigation, and unparalleled stability, redefine your media experience. Elevate every moment with the perfect blend of performance and reliability. It's time to amplify your entertainment journey with the Stable Diffusion XL Base Model!"""

# PROMPT = """Amazon rainforest on the flat Rock in the sunny day in a shopping mall on the desk"""

def get_filepath(root_dir):
    return os.path.join(root_dir, 'upscale' + str(len(os.listdir(root_dir))) + '.png')