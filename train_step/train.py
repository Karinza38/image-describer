from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry

import argparse
import os

print("In train.py")
print("This is where code for training comic reader resides.")

parser = argparse.ArgumentParser("train")

parser.add_argument("--train_image_folder", type=str, help="image data")
parser.add_argument("--train_image_tag", type=str, help="image tag name")

args = parser.parse_args()

print("Argument 1: %s" % args.train_image_folder)
print("Argument 2: %s" % args.train_image_tag)

ENDPOINT = "<CUSTOM-VISION-ENDPOINT>"
training_key = "<CUSTOM-VISION-TRAINING-KEY>"
project_id = "<CUSTOM-VISION-PROJECT-ID>"

trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)
tag_name = args.train_image_tag.replace('-', ' ')

all_tags = trainer.get_tags(project_id)

image_tag = None
for tag in all_tags:
    if tag_name == tag.name:
        image_tag = tag
        break

if not image_tag:
    image_tag = trainer.create_tag(project_id, tag_name)

if args.train_image_folder:
    print("%s Found image folder" % args.train_image_folder)
    print("Adding images...")

    image_list = []
    
    for file_name in os.listdir(args.train_image_folder):
        if file_name.startswith(args.train_image_tag):
            path = os.path.join(args.train_image_folder, file_name)
            with open(path, "rb") as image_contents:
                image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[image_tag.id]))

    upload_result = trainer.create_images_from_files(project_id, images=image_list)
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
        exit(-1)
    else:
        print("Image Upload successfull")


import time

print ("Training...")
iteration = trainer.train_project(project_id)
print(iteration)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project_id, iteration.id)
    print ("Training status: " + iteration.status)
    time.sleep(1)


publish_iteration_name = "comic_describer"
prediction_resource_id = "<CUSTOM-VISITION-PREDICTION-RESOURCE-ID>"

# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project_id, iteration.id, publish_iteration_name, prediction_resource_id)
print ("Published the new model successfully!")