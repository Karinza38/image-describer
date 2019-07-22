import requests
import json
import base64


def get_image_as_byte_array(image_path):
    f = None
    with open(image_path, "rb") as image:
        f = image.read()
        return f   

url = 'https://westus2.api.cognitive.microsoft.com/customvision/v3.0/Prediction/610fd33e-e7c8-4429-a3ac-1dbedcbc3a2e/classify/iterations/Iteration1/image'
image_bytes = get_image_as_byte_array('Images/Riots/test/rioters_burning_car1.JPG')

headers = {"Prediction-Key": "6a9ad0ebebf04268a21377194ff5eaa6",
           "Content-Type": "application/octet-stream"}

r = requests.post(url, data=image_bytes, headers=headers)
print(r.content)
