import requests
import json
import base64

def get_image_data(image_path):
    f = None
    with open(image_path, "rb") as image:
        f = image.read()

    return f

def get_image_description(image_path):
    url = 'https://westus2.api.cognitive.microsoft.com/customvision/v3.0/Prediction/610fd33e-e7c8-4429-a3ac-1dbedcbc3a2e/classify/iterations/image_describer/image'
    image_bytes = get_image_data(image_path)

    headers = {"Prediction-Key": "6a9ad0ebebf04268a21377194ff5eaa6",
               "Content-Type": "application/octet-stream"}

    r = requests.post(url, data=image_bytes, headers=headers)
    return r.content
