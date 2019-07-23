import requests
import json
import base64

def get_image_data(image_path):
    f = None
    with open(image_path, "rb") as image:
        f = image.read()

    return f

def get_image_description(image_path):
    url = ''
    image_bytes = get_image_data(image_path)

    headers = {"Prediction-Key": "",
               "Content-Type": "application/octet-stream"}

    r = requests.post(url, data=image_bytes, headers=headers)
    return r.content
