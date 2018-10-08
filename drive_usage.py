from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.file'

def print_usage(x,y):
    x = int(x)/(1024**3)
    y = int(y)/(1024**3)
    percentage = '{:05.2f}'.format(float(int(x)*100/int(y)))
    message = '{:.2f}'.format(x) + '/' + '{:.2f}'.format(y) + ' (' + percentage +'%)'
    return message
    
def auth(token,credentials):
    store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials, SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    return drive_service

def usage(drive_service):
    about = drive_service.about().get(fields="storageQuota").execute()
    usage = about['storageQuota']['usage']
    limit = about['storageQuota']['limit']
    message = print_user(drive_service) + ' Drive usage: ' + print_usage(usage,limit)
    print(message)
    return usage,limit

def print_user(drive_service):
    user = drive_service.about().get(fields="user").execute()
    email = user['user']['emailAddress']
    return email


drive1usage, drive1limit = usage(auth('token1.json','credentials1.json'))
drive2usage, drive2limit = usage(auth('token2.json','credentials2.json'))

combousage = int(drive1usage) + int(drive2usage)
combolimit = int(drive1limit) + int(drive2limit)
message = 'Combined Drive usage: ' + print_usage(combousage,combolimit)
print(message)