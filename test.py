from list_files import auth,get_file_list,get_root_id,get_user
from pathlib import Path
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