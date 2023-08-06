import os
import asyncio
import requests
# import numpy as np
import json
from PIL import Image
import base64
from io import BytesIO
import re

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

endpoint = 'https://7rq1vzhvxj.execute-api.us-west-1.amazonaws.com/Prod/infer/'
# Endpoint override for development
devmode = False
if 'BoosteURL' in os.environ:
    print("Dev Mode")
    devmode = True
    if os.environ['BoosteURL'] == 'local':
        endpoint = 'http://localhost:8080/2015-03-31/functions/function/invocations'
    else:
        endpoint = os.environ['BoosteURL']
    print("Hitting endpoint:", endpoint)


# to simulate IO
async def waiter(i):
    print(i, "start")
    await asyncio.sleep(i)
    print(i, "end")
    return i


async def api_caller(api_key, prompt, image, forward):
    global endpoint
    port = 8080
    # extension = ":{}/2015-03-31/functions/function/invocations".format(port)
    # url = endpoint + extension
    url = endpoint
    # print(url)

    # defaults
    is_path = False
    is_url = False

    if re.match(url_regex, image) is not None:
        is_url = True

    if os.path.exists(image):
        is_path = True

        if image[-3:] == "jpg" or image[-4:] == "jpeg":
            image_pil = Image.open(image)
            image_file = BytesIO()
            image_pil.save(image_file, format="JPEG")
            image_bytes = image_file.getvalue()  # im_bytes: image in binary format.
            image = base64.b64encode(image_bytes).decode('utf-8')
        elif image[-3:] == "png":
            image_pil = Image.open(image)
            image_file = BytesIO()
            image_pil.save(image_file, format="PNG")
            image_bytes = image_file.getvalue()  # im_bytes: image in binary format.
            image = base64.b64encode(image_bytes).decode('utf-8')
        else:
            print("Warning, image failed: {}\nImage must be .jpg or .png.\n".format(image))
            return None

    if is_path == False and is_url == False:
        print("Warning: image failed: {}\nImage must be valid a URL or a path to local image file\n\texample:  https://google.com\n\texample:  ./my-image.jpg\n\texample:  /home/user/my-image.png\n".format(image))
        return None

    # sequence = []
    payload = {
        "apiKey" : api_key,
        "prompt" : prompt,
        "image" : image,
        "isUrl" : is_url,
        "forward" : forward
    }

    response = requests.post(url, json=payload)
    try:
        if devmode: # then it returns as full json blob
            out = response.json()
            code = out['statusCode']
            body = json.loads(out['body'])
        else:
            # then api gateway converts status code in blob to status code, and body in json to json
            code = response.status_code
            body = response.json()

    except Exception as e:
        print("Warning, server failed to process one request:\n\tprompt:  {}\n\timage:  {}\n".format(prompt, image))
        return None
        
    if code == 200:
        return body
    else:
        raise Exception("Server returned error code {}\n{}".format(code,body))

def softmax_caller(similarities):
    global endpoint
    port = 8080
    extension = ":{}/2015-03-31/functions/function/invocations".format(port)
    url = endpoint + extension

    # sequence = []
    payload = {
        "similarities" : similarities,
        "softmax" : True
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception("Server error: Booste inference server returned status code {}\n{}".format(
            response.status_code, response.json()['message']))
    try:
        out = response.json()

        # if out['statusCode'] == 200:
        #     return json.loads(out['body'])
        # else:
        #     return None
    except:
        out = None
        raise Exception("Server error: Failed to return taskID")

# # correct solution:
# def softmax(x):
#     """Compute softmax values for each sets of scores in x."""
#     e_x = np.exp(x - np.max(x))
    # return e_x / e_x.sum(axis=0) # only difference

async def clip_main(api_key, prompts, images, forward):

    if type(prompts) != type([]):
        raise Exception("Error: prompts not of type: list")
    
    if type(images) != type([]):
        raise Exception("Error: images not of type: list")

    if prompts == []:
        raise Exception("Error: prompts cannot be length: 0")
    else:
        for item in prompts:
            if type(item) != type(""):
                raise Exception("Error: all prompts must be type: string")

    if images == []:
        raise Exception("Error: images cannot be length: 0")
    else:
        for item in images:
            if type(item) != type(""):
                raise Exception("Error: all images must be type: string")


    tasks = {}
    for prompt in prompts:
        tasks[prompt] = {}
        for image in images:
            tasks[prompt][image] = asyncio.create_task(api_caller(api_key, prompt, image, forward))

    outs = {}
    # out_logits = np.zeros((len(images), len(prompts)))
    # print(out_logits)
    for i, prompt in enumerate(prompts):
        outs[prompt] = {}
        for j, image in enumerate(images):
            out = await tasks[prompt][image]
            outs[prompt][image] = out
            # out_logits[i,j] = out['similarity']

    # softmax_caller(out_logits.tolist())
    
    return outs

def clip_image_main(images):
    return dict_out

def clip_text_main(prompts):
    return dict_out

def clip_fast_main(prompts, images, forward):
    return dict_out