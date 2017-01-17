import httplib2
import os
import argparse

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    '''
    Gets valid user credentials from storage.
    
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    
    Returns:
        Credentials, the obtained credential.
    '''    
    
    credential_dir = "/home/pi/SmartScale/sheets_client_secret.json "
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
        'sheets.googleapis.com-python-quickstart.json')
        store = Storage(credential_path)    
        credentials = store.get()    
        if not credentials or credentials.invalid:        
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)        
        flow.user_agent = APPLICATION_NAME        
        if flags:            
        credentials = tools.run_flow(flow, store, flags)        
        else: # Needed only for compatibility with Python 2.6            
        credentials = tools.run(flow, store)        
        print('Storing credentials to ' + credential_path)    
        return credentials
