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

def lcd_msg_formatter(txt, cols):
    '''
    Formats a string into a list of strings to be printed out on the LCD
    Note that for now the LCD MUST have 2 rows
    Any number of columns
    Args:
        txt: string
        cols: int
    Returns:
        messages: list of strings perfectly formatted for an Adafruit LCD
    '''
    messages = []
    txt_copy = ''
    for i in txt:
        txt_copy += i

    msg = ''
    while len(txt_copy) > 0:
        if len(txt_copy) < cols:
            msg += txt_copy
            messages += [msg]
            break
            
        lastCharIdx = cols
        for j in range(cols + 1):
            if txt[(cols + 1) - j] == ' ' or txt[(cols + 1) - j] == '-':
                lastCharIdx = ((cols + 1) - j)
                break
                
        if len(msg) == 0:
            for i in range(lastCharIdx):
                msg += txt_copy[i]
            msg += '\n'
            txt_copy = txt_copy[(lastCharIdx - 1):]
        else:
            for i in range(lastCharIdx):
                msg += txt_copy[i]
            messages += [msg]
            msg = ''
            txt_copy = txt_copy[(lastCharIdx - 1):]
            
    return messages
        
        
                
        
