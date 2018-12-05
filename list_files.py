from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload
import json
import pprint
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


kb = lambda x : int(x) / (1024**1)
mb = lambda x : int(x) / (1024**2)
gb = lambda x : int(x) / (1024**3)

def auth(token,credentials):
    store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials, SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    return drive_service

def list_files(drive_service,number_of_files):
    i = 0
    pageToken = 0
    if number_of_files < 100:
        pageSize = number_of_files
    else:
        pageSize = 100
    while i<number_of_files:
        if i==0:
            root_id = drive_service.files().get(fileId="root").execute()['id']
            print(root_id)
            results = drive_service.files().list(pageSize=pageSize,fields="nextPageToken, files(id,name,size,parents,mimeType)").execute()
        else:
            results = drive_service.files().list(pageSize=pageSize,pageToken=pageToken,fields="nextPageToken, files(id,name,size,mimeType)").execute()
        items = results.get('files', [])
        pageToken = results.get('nextPageToken')
        if not items:
            print("Files not found")
        else:
            for item in items:
                if 'size' not in item:
                    if item['mimeType'] == "application/vnd.google-apps.folder":
                        print('{0}.{1} ({2}), Directory'.format(i+1,item['name'], item['id']))
                    else:
                        print('{0}.{1} ({2}), Size: Not Available'.format(i+1,item['name'], item['id']))
                        print(item['mimeType'])
                    
                else:
                    print('{0}.{1} ({2}), Size: '.format(i+1,item['name'], item['id'])+'{:.2}'.format(mb(item['size'])) + ' Mb')
                i+=1
        if not pageToken:
            break















# file_number = int(input('Number of file you want to download?\n'))
# onefile = total[file_number]
# print(onefile)
# filename = onefile['name']
# file_id=onefile['id']
# # FILE DOWNLOADING
# request = service.files().get_media(fileId=file_id)
# fh = io.FileIO(filename,'wb')
# downloader = MediaIoBaseDownload(fh, request)
# done = False
# while done is False:
#     status, done = downloader.next_chunk()
#     print("Download %d%%." % int(status.progress() * 100))