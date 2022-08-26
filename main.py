import shutil
import os
import win32api
import datetime
from pathlib import Path
from sys import platform

nas_path = '//mycloudex2ultra/christoph/CanonIngest'


def get_sd_card_canon_folder():

    if platform == 'win32':
        drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
    else:
        drives =

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
        Path(nas_path + '/' + date).mkdir(parents=True, exist_ok=True)


def copy_files():
    source_folder = get_sd_card_canon_folder()

    copied_files = 0

    create_folders(source_folder)

    for file in os.listdir(source_folder):
        file_cdate = datetime.datetime.fromtimestamp(os.path.getctime(source_folder + '/' + file))
        trimmed_date = file_cdate.strftime('%Y-%m-%d')

        source_file_path = source_folder + '/' + file
        target_file_path = nas_path + '/' + trimmed_date + '/' + file

        if not os.path.exists(target_file_path):
            print('copying file ' + source_file_path)
            shutil.copy2(source_file_path, target_file_path)
            copied_files += 1

    print('copied ' + copied_files.__str__() + ' files')


if __name__ == '__main__':
    copy_files()