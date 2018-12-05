from list_files import auth,get_file_list,get_root_id
from pathlib import Path
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import sys


FOLDER = 'application/vnd.google-apps.document'

print("Number of arguments " + str(len(sys.argv)))

token_path = Path("Tokens/")
credentials_path=Path("Credentials/")

def make_children(fileList):
        for i in fileList:
            i['children'] = []
            for j in fileList:
                if('parents' in j):
                    if(j['parents'][0]==i['id']):
                        i['children'].append(j['id'])



i = 1
token = token_path / ("token00" + str(i) + ".json")
credentials = credentials_path / ("credentials00" + str(i) + ".json")
fileList = get_file_list(auth(token,credentials),200)
drive = auth(token,credentials)
root_id = get_root_id(auth(token,credentials))

def get_file_name(id,fileList):
    for i in fileList:
        if(i['id']==id):
            return i['name']
make_children(fileList)


def get_contents(id,fileList):
    content = []
    for i in fileList:
        if('parents' in i):
            if(i['parents'][0]==id):
                content.append(i)
    return content
    

def rekt(id,fileList,level=0):
    # print("Doing rekt for " + str(id))
    for k in fileList:
        if(k['id']==id):
            if(level==1):
                print(' +' + k['name'])
            else:
                print((level-1)*' |' + ' +' + k['name'])
    for i in get_contents(id,fileList):
        rekt(i['id'],fileList,level+1)



for i in fileList:
    print(i)

print("")

rekt(root_id,fileList)




# file_metadata = {'name': 'igor.jpg'}
# media = MediaFileUpload('igor.jpg', mimetype='image/jpeg')
# file = drive.files().create(body=file_metadata,media_body=media,fields='id').execute()
# print('File ID: ' + file.get('id'))

# list_files.list_files(list_files.auth(token,credendtials),100)

#test



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