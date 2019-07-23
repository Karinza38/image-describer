import comics_transcript_extractor as ComicsTranscriptExtractor

import os
import requests
import time
from xml.etree import ElementTree

import json


class TextToSpeech(object):
    def __init__(self, subscription_key, transcript):
        self.subscription_key = subscription_key
        self.tts = transcript
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
    
    def get_token(self):
        fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'Text-to-Speech'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)')
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open('sample-' + self.timestr + '.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) +
                    "\nYour TTS is ready for playback.\n")
        else:
            print(response.content)
            print("\nStatus code: " + str(response.status_code) +
                "\nSomething went wrong. Check your subscription key and headers.\n")


if __name__ == "__main__":
    with open("keys.json", 'r') as f:
        keys = json.load(f)
    
    subscription_key = keys['text_to_speech']['subscription_key']
    transcript = ComicsTranscriptExtractor.get_transcript("Comics/the_monkey_and_the_dog.htm", keys)
    print("Got the transcript. Now giving it the voice...")
    app = TextToSpeech(subscription_key, transcript)
    app.get_token()
    app.save_audio()

#print(ImageDescriber.get_image_description('Images/Animals/Monkey/Test/monkey_with_dog.JPG'))