#!/usr/bin/python

import time
import Adafruit_CharLCD as LCD
from googlefinance import getQuotes

from oauth2client.client import flow_from_clientsecrets
FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope = 'https://www.googleapis.com/auth/analytics.readonly',
    message = '%s is missing' % CLIENT_SECRETS)

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

# Printing some messages
tickers = ['AAPL', 'GS', 'DB', 'GORO']

while True:
    for ticker in tickers:
        lcd.clear()
        ticker_json = getQuotes(ticker)[0]
        price = ticker_json['LastTradePrice']
        myTime = ticker_json['LastTradeTime']
        msg = ticker + ': ' + price + '\nat ' + myTime
        lcd.message(msg)
        time.sleep(2.0)
