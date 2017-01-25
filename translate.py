import requests

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
                txt_copy = txt_copy[(lastCharIdx + 1):]
            else:
                for i in range(lastCharIdx):
                    msg += txt_copy[i]
                messages += [msg]
                msg = ''
                txt_copy = txt_copy[(lastCharIdx + 1):]
    return messages


txt = 'hello my name is roman and I love to program and make things out of electronics'
fermerted = lcd_msg_formatter(txt, 16)
print(fermerted)
        
                
        
