from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.file'

kb = lambda x : int(x) / (1024**1)
mb = lambda x : int(x) / (1024**2)
gb = lambda x : int(x) / (1024**3)

def get_usage_formated(x,y):
    x = gb(x)
    y = gb(y)
    percentage = '{:05.2f}'.format(float(int(x)*100/int(y)))
    message = '{:.2f}'.format(x) + '/' + '{:.2f}'.format(y) + ' (' + percentage +'%)'
    return message

def get_usage(drive_service):
    about = drive_service.about().get(fields="storageQuota").execute()
    usage = about['storageQuota']['usage']
    return usage


def get_limit(drive_service):
    about = drive_service.about().get(fields="storageQuota").execute()
    limit = about['storageQuota']['limit']
    return limit
    
def get_user(drive_service):
    user = drive_service.about().get(fields="user").execute()
    email = user['user']['emailAddress']
    return email

