#!/usr/bin/python

import time
import Adafruit_CharLCD as LCD

import argparse
import base64
import json
import httplib2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# Raspberry Pi pin configuration:
lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)

# Setting up Google Cloud Speech API
DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                 'version={apiVersion}')

def get_speech_service():
    '''
    Uses application default credentials to authorize google api requests
    Note that environment variables:
        GOOGLE_APPLICATION_CREDENTIALS must be set to the path of service credentials json
        GCLOUD_PROJECT must be set to the name of your project
        * I did this in the bash file *
    Returns:
        Google Cloud Speech API service
    '''
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build(
        'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)


def main(speech_file):
    '''
    Transcribe the given audio file and prints it on the lcd

    Args:
        speech_file: the name of the audio file.
    '''
    with open(speech_file, 'rb') as speech:
        speech_content = base64.b64encode(speech.read())

    service = get_speech_service()
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                'encoding': 'linear16',
                'sampleRate': 16000,
                'languageCode': 'en-US',
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    
    response = service_request.execute()
    
    # Unwrapping the json
    json_results = json.dumps(response)
    results = json.loads(json_results)['results']
    
    result_string = ''
    for result in results:
        alternatives = result['alternatives']
    
        for alternative in alternatives:
            transcript = alternative['transcript']
        
            for transcript_char in transcript:
                result_string += transcript_char
            
    lcd.message(result_string)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'speech_file', help='/Users/roman/Desktop/audio.raw')
    args = parser.parse_args()
    main(args.speech_file)
