from list_files import auth,list_files
from pathlib import Path
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

token_path = Path("Tokens/")
credentials_path=Path("Credentials/")

i = 2
token = token_path / ("token00" + str(i) + ".json")
credentials = credentials_path / ("credentials00" + str(i) + ".json")
list_files(auth(token,credentials),100)


drive = auth(token,credentials)

# file_metadata = {'name': 'igor.jpg'}
# media = MediaFileUpload('igor.jpg', mimetype='image/jpeg')
# file = drive.files().create(body=file_metadata,media_body=media,fields='id').execute()
# print('File ID: ' + file.get('id'))

# list_files.list_files(list_files.auth(token,credendtials),100)

#test