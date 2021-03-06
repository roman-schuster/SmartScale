#!/usr/bin/python

import time                                         # waiting between lcd messages
import Adafruit_CharLCD as LCD                      # for LCD

import argparse                                     # for getting the wav file from command line
import base64                                       # for encoding the wav file to send to Google Speech API
import json                                         # for unwrapping the Google Speech API response
import httplib2                                     # for sending the Google Speech API request

from googleapiclient import discovery               # for accessing Google Speech Service
from oauth2client.client import GoogleCredentials   # for authorizing Google Speech Service

import requests                                     # for Microsoft Translate services

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

  
def format_string_for_lcd(lcd_columns, lcd_rows, text_string):
    '''
    Returns a list of strings to print on a lcd_columns x lcd_rows display
    Each string is lcd_columns long and contains (lcd_rows - 1) newlines
    There will be at least len(text_string)/(lcd_columns*lcd_rows) elements
    and at max (len(text_string)/(lcd_columns*lcd_rows) + 1) elements
    '''
    list_of_strings = []
    temp_string = ''
    
    for i in range(len(text_string)):
        if len(temp_string) == (lcd_columns - 1):
            temp_string += ('\n' + text_string[i])
        else:
            temp_string += text_string[i]
        
        if i == (len(text_string) - 1):
            list_of_strings += [temp_string]
        elif (len(temp_string) != 0) and (len(temp_string) % ((lcd_columns*lcd_rows) - 1)) == 0:
            list_of_strings += [temp_string]
            temp_string = ''

    return list_of_strings

  
def translate_text(txt = 'Please enter some text', from_lang = 'en', to_lang = 'fr'):
    '''
    Runs authentication for Microsoft Translate service on Azure Marketplace
    Args:
        txt: string
        from_lang: string - must be a valid country code
        to_lang: string - must be a valid country code
    Returns:
        string containing the translation of txt from from_lang to to_lang
    '''
    # Authenticating
    auth_key = '7d2c5a67c24c45ce90fc219a3fae8bf9'
    auth_url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
    auth_headers = {'Ocp-Apim-Subscription-Key' : auth_key}
    auth_response = requests.post(auth_url, headers = auth_headers)
    token = auth_response.text

    # Translating
    translate_url = 'https://api.microsofttranslator.com/v2/http.svc/Translate'
    translate_params = { 'appid' : ('Bearer ' + token), 'text' : txt, 'from' : from_lang, 'to' : to_lang}
    translate_headers = {'Accept' : 'application/xml'}
    translate_response = requests.get(translate_url, params = translate_params, headers = translate_headers)
    
    # Ooooooweeee translate_response.txt has some weird ass HTML formatting to clean up
    # There are 68 useless chars at the beginning and 9 at the end to get rid of
    FIRST_REAL_CHAR = 68
    LAST_REAL_CHAR = len(translate_response.text) - 9
    return translate_response.text[FIRST_REAL_CHAR:LAST_REAL_CHAR]


    
def main(speech_file):
    '''
    Transcribe the given audio file, translates it, and prints it out

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
                'profanityFilter': False,
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    
    response = service_request.execute()
    
    # Unwrapping the json
    result_string = '' # The final string containing the text we translated
    json_results = json.dumps(response)
    results = json.loads(json_results)['results']
    for result in results:
        alternatives = result['alternatives']
    
        for alternative in alternatives:
            transcript = alternative['transcript']
        
            for i in range(len(transcript)):
                result_string += transcript[i]
    
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
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
    
    translated_string = translate_text(result_string)

    messages = format_string_for_lcd(lcd_columns, lcd_rows, translated_string)
    for msg in messages:
        lcd.clear()
        lcd.message(msg)
        time.sleep(3.0)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'speech_file', help='/Users/roman/Desktop/audio.raw')
    args = parser.parse_args()
    main(args.speech_file)
