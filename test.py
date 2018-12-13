from drive_lib import auth,get_file_list,get_root_id,get_user,tree,get_file_name,get_file,download_file
# from pathlib import Path
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import sys,os





# file_metadata = {'name': 'igor.jpg'}
# media = MediaFileUpload('igor.jpg', mimetype='image/jpeg')
# file = drive.files().create(body=file_metadata,media_body=media,fields='id').execute()
# print('File ID: ' + file.get('id'))


drive_service = auth('./Token/token003.json','./Credentials/credentials003.json')

# fileList = get_file_list(drive_service,200)

# root_id = get_root_id(drive_service)

# print(' + root')
# tree(root_id,fileList,0)

# #test
# for i in fileList:
#     print(i)




# file_id = str(input('Id of the file you want to download?\n'))

# mimeType = get_file(file_id,fileList)['mimeType']

# print(mimeType)
# fileName = get_file_name(file_id,fileList)

# download_file(file_id,fileList,drive_service)


# # # FILE DOWNLOADING
# # export
# request = drive_service.files().export_media(fileId=file_id,
#                                              mimeType='application/pdf')
# fh = io.BytesIO()
# downloader = MediaIoBaseDownload(fh, request)
# done = False
# while done is False:
#     status, done = downloader.next_chunk()
#     print "Download %d%%." % int(status.progress() * 100)


# # download
# filename = get_file_name(file_id,fileList)
# request = drive_service.files().get_media(fileId=file_id)
# fh = io.FileIO(filename,'wb')
# downloader = MediaIoBaseDownload(fh, request)
# done = False
# while done is False:
#     status, done = downloader.next_chunk()
#     print("Download %d%%." % int(status.progress() * 100))