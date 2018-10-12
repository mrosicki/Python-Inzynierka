from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload
import json
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'


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
    if number_of_files < 100:
        pageSize = number_of_files
    else:
        pageSize = 100
    while i<number_of_files:
        if i==0:
            results = drive_service.files().list(pageSize=pageSize,fields="nextPageToken, files(id,name,size)").execute()
        else:
            results = drive_service.files().list(pageSize=pageSize,pageToken=pageToken,fields="nextPageToken, files(id,name,size)").execute()
        items = results.get('files', [])
        pageToken = results.get('nextPageToken')
        if not items:
            print("Files not found")
        else:
            for item in items:
                if 'size' not in item:
                    print(u'{0}.{1} ({2}), Size: Not Available'.format(i+1,item['name'], item['id']))
                else:
                    size_mb = float(item['size'])/(1024**2) 
                    print(u'{0}.{1} ({2}) '.format(i+1,item['name'], item['id'])+'{:.2}'.format(size_mb) + ' Mb')
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