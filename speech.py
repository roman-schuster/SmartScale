#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 12:13:26 2017

@author: roman
"""

import argparse
import base64
import json
import httplib2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                 'version={apiVersion}')

def get_speech_service():
    """
    Authorizes 
    """
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build(
        'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)
    
    
    
    
def main(speech_file):
    """Transcribe the given audio file.

    Args:
        speech_file: the name of the audio file.
    """
    with open(speech_file, 'rb') as speech:
        speech_content = base64.b64encode(speech.read())

    service = get_speech_service()
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                'encoding': 'linear16',  # wav 16-bit signed LE samples
                'sampleRate': 16000,  # 16 khz
                'languageCode': 'en-US',  # a BCP-47 language tag
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    response = service_request.execute()
    response_json = json.dumps(response)
    
    results = response['results']
    text_string = ''
    for alt in results:
      alternative = alt['alternatives']
      transcript = alternative['transcript']
      for single_character in transcript:
        text_string += single_character
    
    print('You said: ' + text_string)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'speech_file', help='/Users/roman/Desktop/audio.raw')
    args = parser.parse_args()
    main(args.speech_file)    
    
    
    
    
    
    
    
