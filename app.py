from drive_lib import auth,get_file_list,get_root_id,get_user,tree,get_file_name,get_file,download_file,get_emails,print_file_list
# from pathlib import Path
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import sys,os
import time
# from clear import clear



print('=======================================================================')
print('|                                                                     |')
print('|                                                                     |')
print('|                   Welcome to google drive manager                   |')
print('|                                                                     |')
print('|              please wait while your drives are loading              |')
print('|                                                                     |')
print('|             type help to see list of available commands             |')
print('|                                                                     |')
print('=======================================================================')
drives = []
for i in range(1,len(os.listdir('./Token'))+1):
    Token = './Token/token00' + str(i) + '.json'
    Credentials = './Credentials/credentials00' + str(i) + '.json'
    drive_service = auth(Token,Credentials)
    drives.append(drive_service)
time.sleep(4)
os.system('clear')

while(True):
    string = raw_input('Drive> ')
    if(string=='help'):
        print('Following commands are available:')
        print('emails\t\tshows emails whose drives are currently available')
        print('ls\t\tshows contents of drive')
        print('download\tdownloads a file from drive')
        print('clear\t\tclears console')
        print('tree\t\tshows structure of a drive')
        print('quit\t\texits the program')
    elif('emails'==string):
        emails = get_emails()
        for k,v in emails.items():
            print(v)
    elif('ls'==string):
        emails = get_emails()
        for k,v in emails.items():
            print(str(k) +' '+v)
        mail = raw_input('Which drive to list?(number) ')
        print_file_list(drives[int(mail)-1])
    elif('download'==string):
        emails = get_emails()
        for k,v in emails.items():
            print(str(k) +' '+v)
        drive = raw_input('From which drive?(number) ')
        file_id = raw_input('Put file id ')
        download_file(file_id,get_file_list(drives[int(drive)-1]),drives[int(drive)-1])
    elif('clear'==string):
        os.system('clear')
    elif('tree'==string):
        emails = get_emails()
        for k,v in emails.items():
            print(str(k) +' '+v)
        drive = raw_input('Which drive? ')
        print(' +root')
        tree(get_root_id(drives[int(drive)-1]),get_file_list(drives[int(drive)-1]))
        file_id = raw_input('Put file id ')
        download_file(file_id,get_file_list(drives[int(drive)-1]),drives[int(drive)-1])
    elif('clear'==string):
        os.system('clear')
    elif('tree'==string):
        emails = get_emails()
        for k,v in emails.items():
            print(str(k) +' '+v)
        drive = raw_input('Which drive? ')
        print(' +root')
        tree(get_root_id(drives[int(drive)-1]),get_file_list(drives[int(drive)-1]))
    elif('quit'==string):
        break
    else:
        print('Wrong command')
    