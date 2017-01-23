import requests

def translate_text(txt = 'Please enter some text', from_lang = 'en', to_lang = 'fr'):
    '''
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
    return translate_response.text
