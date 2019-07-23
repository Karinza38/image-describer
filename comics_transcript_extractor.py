from bs4 import BeautifulSoup
import image_describer as ImageDescriber

def get_transcript(comics_file, keys_obj):
    soup = None
    with open(comics_file, "r", encoding='utf8') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
    
    comic_content_div = soup.findAll("div", {"class": "col-md-9 col-lg-9 col-sm-8 contLft"})[0]

    title = get_title(comic_content_div)
    scenes = get_scenes(comic_content_div, keys_obj)

    transcript = "Hi, I am gonna help you read this comics story: " + title + ". Here's what will happen: For each scene, I am gonna call out what I see in the image, and rest I am gonna leave to your imagination. So, let's get started. " + scenes
    return transcript

def get_title(comic_content_div):
    return comic_content_div.find("h2").text

def get_scenes(comic_content_div, keys_obj):
    scenes = comic_content_div.findAll("div", {"class": "col-md-6 col-lg-6 col-sm-6 comicWrap"})
    scene_transcript_list = []
    scene_index = 1
    for scene in scenes:
        image_src = "Comics/" + scene.find("img")['src']
        image_decription = ImageDescriber.get_image_description(
            image_src, 
            keys_obj['custom_vision_api']['url'],
            keys_obj['custom_vision_api']['prediction_key'])
        image_decription = 'Scene ' + str(scene_index) + ': I see, ' + image_decription + '.'

        print(image_decription)

        text = scene.text
        complete_text = image_decription + " " + text.strip()
        scene_transcript_list.append(complete_text)
        scene_index += 1

    return '\n'.join(scene_transcript_list)

