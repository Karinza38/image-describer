#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License.

from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials
import urllib.request
import requests
import shutil
import argparse
import os

print("In image_scrapper.py")
print("This is where image is scrapped.")

parser = argparse.ArgumentParser("scrapper")

parser.add_argument("--scrapper_output_folder", type=str, help="image output folder")
parser.add_argument("--scrapper_image_tag", type=str, help="image tag name")
parser.add_argument("--scrapper_search_term", type=str, help="scrapper search term")

args = parser.parse_args()

print("Argument 1: %s" % args.scrapper_output_folder)
print("Argument 2: %s" % args.scrapper_image_tag)
print("Argument 3: %s" % args.scrapper_search_term)

subscription_key = "<YOUR_SUBSCRIPTION_KEY>"
search_term = args.scrapper_search_term

client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))

image_results = client.images.search(query=search_term)

if image_results.value:
    print("Total number of images returned: {}".format(len(image_results.value)))

    for i in range(0, min(50, len(image_results.value))):
        image_result = image_results.value[i]
        content_url = image_result.content_url

        os.makedirs(args.scrapper_output_folder + "/" + args.scrapper_image_tag, exist_ok=True)
        path = os.path.join(args.scrapper_output_folder + "/" + args.scrapper_image_tag, args.scrapper_image_tag + str(i))

        try:
            r = requests.get(content_url, stream=True)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        except:
            continue
else:
    print("No image results returned!")







