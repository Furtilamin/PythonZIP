from shutil import rmtree
from os import path, remove, chdir, mkdir, getcwd, listdir
from datetime import datetime
from zipfile import ZipFile
from yadisk import YaDisk, exceptions


def today_check(files_path):
    files_arr = []
    chdir(give_path(files_path))
    for k in listdir(path.abspath(getcwd())):
        if (datetime.now().day - datetime.fromtimestamp(path.getmtime(k)).day) <= 1:
            files_arr.append(k)
    return files_arr


def zippy(files_path):
    if path.exists(files_path):
        chdir(give_path(files_path))
        try:
            mkdir(path.dirname(getcwd()) + '/zippy')
        except FileExistsError:
            pass
        zip_path = (path.dirname(getcwd()) + '/zippy')
        zip_f = ZipFile(zip_path + '/today_files.zip', 'w')
        files_list = today_check(getcwd())
        for i in files_list:
            print('Today file %s is received' % i)
            zip_f.write(i)
        chdir(path.dirname(getcwd()))
        if not zip_f.namelist():
            print('Today files are missing!')
            return -1
        else:
            print('Today files are successfully archived!')
            return 0
    else:
        print('Incorrect path, try again!')
        return 1


def upload_file(path_to, token):
    y = YaDisk(token=token)
    path_from = getcwd() + '/zippy/today_files.zip'
    try:
        if y.exists(path_to):
            y.upload(give_path(path_from), path_to, overwrite=True)
            print('Archive successfully uploaded!')
            return 0
        else:
            print('Incorrect path to Yandex.Disk')
            return -1
    except exceptions.UnauthorizedError:
        print('Wrong token!')
        return 1


def give_path(path_file):
    return path.abspath(path_file)


def remove_file(files_path):
    delete_arr = today_check(files_path)
    for i in delete_arr:
        print('File %s has been deleted' % i)
        remove(i)
    return 0


def remove_zip():
    zip_path = getcwd() + '/zippy'
    if path.isdir(zip_path):
        rmtree(zip_path)
        return 0
    else:
        return 1


def main(files_path, yad_dst_path, token):
    if zippy(give_path(files_path)) == 0:
        if upload_file(yad_dst_path, token) == 0:
            remove_zip()
            remove_file(give_path(files_path))
            chdir(path.dirname(getcwd()))
            return 0
        else:
            remove_zip()
            return 1
    else:
        remove_zip()
        return -1
