import shutil
import os
import datetime
import sys
from pathlib import Path
from sys import platform
import subprocess
import ftplib


sd_card_label = 'EOS_DIGITAL'
ftp_address = '192.168.178.101'

def get_nas_path():
  if platform == 'win32':
    return '//mycloudex2ultra/christoph/CanonIngest'

  return'/media/mycloudex2ultra/CanonIngest'



def get_sd_card_canon_folder():
    if platform == 'win32':
        import win32api
        drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
        canon_folder = ''
        for drive in drives:
            clean_string = drive.replace('\\', '')
            folders = os.listdir(clean_string)

            for folder in folders:
                if folder == 'DCIM':
                    for f in os.listdir(drive + 'DCIM'):
                        if f == '100CANON':
                            canon_folder = drive + 'DCIM\\100CANON'
                    break

        print('Canon folder is ' + canon_folder)
        return canon_folder

    else:
        try:
            os.system('mount -L ' + sd_card_label + ' /media/CANON_SD/')
            print(os.listdir('/media/CANON_SD/DCIM'))
            return '/media/CANON_SD/DCIM/100CANON'
        except Exception as e:
            print('SD Card not found')
            print(e)
            sys.exit(1)



def get_unique_dates(source_folder):
    unique_dates = []
    for file in os.listdir(source_folder):
        file_cdate = datetime.datetime.fromtimestamp(os.path.getctime(source_folder + '/' + file))
        trimmed_date = file_cdate.strftime('%Y-%m-%d')

        if trimmed_date not in unique_dates:
            unique_dates.append(trimmed_date)

    return unique_dates


def create_folders(source):
    for date in get_unique_dates(source):
        print(get_nas_path())
        print(date)
        Path(get_nas_path() + '/' + date).mkdir(parents=True, exist_ok=True)


def copy_files():
    source_folder = get_sd_card_canon_folder()

    copied_files = 0

    create_folders(source_folder)

    for file in os.listdir(source_folder):
        file_cdate = datetime.datetime.fromtimestamp(os.path.getctime(source_folder + '/' + file))
        trimmed_date = file_cdate.strftime('%Y-%m-%d')

        source_file_path = source_folder + '/' + file
        target_file_path = get_nas_path() + '/' + trimmed_date + '/' + file

        if not os.path.exists(target_file_path):
            print('copying file ' + source_file_path)
            #shutil.copy2(source_file_path, target_file_path)
            #os.system('cp ' + source_file_path + ' ' + 'target_file_path')
            session = ftplib.FTP(ftp_address, 'christoph', 'malvado6696')
            file_to_send = open(source_file_path, 'rb')
            session.storbinary('canonIngest/' + trimmed_date + '/' + file, file_to_send)
            file_to_send.close()
            copied_files += 1

    print('copied ' + copied_files.__str__() + ' files')
    session.quit()


if __name__ == '__main__':
    copy_files()
