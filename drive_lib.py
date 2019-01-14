from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io,os
from googleapiclient.http import MediaIoBaseDownload
import json
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


kb = lambda x : float(x) / (1024**1)
mb = lambda x : float(x) / (1024**2)
gb = lambda x : float(x) / (1024**3)

def auth(token,credentials):
    store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials, SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    return drive_service

def get_file_list(drive_service,number_of_files=999999999):
    i = 0
    pageToken = 0
    fileList = []
    if number_of_files < 100:
        pageSize = number_of_files
    else:
        pageSize = 100
    while i<number_of_files:
        if i==0:
            # root_id = drive_service.files().get(fileId="root").execute()['id']
            # # print(root_id)
            results = drive_service.files().list(pageSize=pageSize,fields="nextPageToken, files(id,name,size,parents,mimeType)").execute()
        else:
            results = drive_service.files().list(pageSize=pageSize,pageToken=pageToken,fields="nextPageToken, files(id,name,size,mimeType)").execute()
        items = results.get('files', [])
        pageToken = results.get('nextPageToken')
        if not items:
            # print("Files not found")
            break
        else:
            for item in items:
                # if 'size' not in item:
                #     if item['mimeType'] == "application/vnd.google-apps.folder":
                #         print('{0}.{1} ({2}), Directory'.format(i+1,item['name'], item['id']))
                #     else:
                #         print('{0}.{1} ({2}), Size: Not Available'.format(i+1,item['name'], item['id']))
                #         print(item['mimeType'])
                    
                # else:
                #     print('{0}.{1} ({2}), Size: '.format(i+1,item['name'], item['id'])+'{:.2}'.format(mb(item['size'])) + ' Mb')
                fileList.append(item)
                i+=1       
        if not pageToken:
            break
    return fileList



def print_file_list(drive_service,number_of_files=999999999):
    i = 0
    pageToken = 0
    fileList = []
    if number_of_files < 100:
        pageSize = number_of_files
    else:
        pageSize = 100
    while i<number_of_files:
        if i==0:
            # root_id = drive_service.files().get(fileId="root").execute()['id']
            # # print(root_id)
            results = drive_service.files().list(pageSize=pageSize,fields="nextPageToken, files(id,name,size,parents,mimeType)").execute()
        else:
            results = drive_service.files().list(pageSize=pageSize,pageToken=pageToken,fields="nextPageToken, files(id,name,size,mimeType)").execute()
        items = results.get('files', [])
        pageToken = results.get('nextPageToken')
        if not items:
            print("Files not found")
            break
        else:
            for item in items:
                if 'size' not in item:
                    if item['mimeType'] == "application/vnd.google-apps.folder":
                        print('{0}.{1} ({2}), Directory'.format(i+1,item['name'], item['id']))
                    else:
                        print('{0}.{1} ({2}), Size: Not Available'.format(i+1,item['name'], item['id']))
                        # print(item['mimeType'])                   
                else:
                    print('{0}.{1} ({2}), Size: '.format(i+1,item['name'], item['id'])+'{:.2}'.format(mb(item['size'])) + ' Mb')
                fileList.append(item)
                i+=1       
        if not pageToken:
            break
    return fileList


def get_root_id(drive_service):
    root_id = drive_service.files().get(fileId="root").execute()['id']
    return root_id

def make_children(fileList):
        for i in fileList:
            i['children'] = []
            for j in fileList:
                if('parents' in j):
                    if(j['parents'][0]==i['id']):
                        i['children'].append(j['id'])

def get_file_name(id,fileList):
    for i in fileList:
        if(i['id']==id):
            return i['name']

def get_file(id,fileList):
    for i in fileList:
        if(i['id']==id):
            return i

def get_contents(id,fileList):
    content = []
    for i in fileList:
        if('parents' in i):
            if(i['parents'][0]==id):
                content.append(i)
    return content

def tree(id,fileList,level=0):
    # print("Doing rekt for " + str(id))
    for k in fileList:
        if(k['id']==id):
            if(level==0):
                print(' +' + k['name'])
            else:
                print((level)*' |' + ' +' + k['name'])
    for i in get_contents(id,fileList):
        tree(i['id'],fileList,level+1)

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

def get_emails():
    users = {}
    for i in range (1,len(os.listdir('./Token'))+1):
        token = './Token/token00' + str(i) +'.json'
        credendtials = './Credentials/credentials00' + str(i) + '.json'
        user = get_user(auth(token,credendtials))
        users[i] = user
    return(users)

def download_file(file_id,fileList,drive_service):
    mimeType = get_file(file_id,fileList)['mimeType']
    fileName = get_file_name(file_id,fileList)
    if('application/vnd.google-apps.' in mimeType):
        if('document' in mimeType):
            # print('This is a document')
            conversion = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            fileName = fileName + '.docx'
        elif('spreadsheet' in mimeType):
            # print('This is a sheet')
            conversion = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            fileName = fileName + '.xls'
        elif('presentation' in mimeType):
            # print('This is a presentation')
            conversion = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            fileName = fileName + '.ppt'
        else:
            conversion = 'application/pdf'
            fileName = fileName + '.pdf'
        request = drive_service.files().export_media(fileId=file_id,mimeType=conversion)
        # print('Tak')
    else:
        request = drive_service.files().get_media(fileId=file_id)
        # print('Nie')
    fh = io.FileIO(fileName,'wb')
    downloader = MediaIoBaseDownload(fh,request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))

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