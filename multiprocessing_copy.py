import shutil
import os
import time
import random
from multiprocessing import Pool
from functools import partial
import json
# Natali Kuskova


def get_threads_number(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        entry = json.load(f)
        f.close()
        return entry['threads_number']


def get_files_path():
    from_fullname = []
    to_fullname = []
    from_path = input('Введите путь к каталогу из которого '
                      'нужно скопировать файлы: ')
    to_path = input('Введите путь к каталогу, в который '
                    'нужно скопировать файлы: ')
    if os.path.exists(from_path) and os.path.exists(to_path):
        # список файлов и поддиректорий в данной директории
        names = os.listdir(from_path)
        for name in names:
            # получить полное имя
            f_name = os.path.join(from_path, name)
            # если это файл
            if os.path.isfile(f_name):
                from_fullname.append(f_name)
                to_fullname.append(os.path.join(to_path, name))
        return from_fullname, to_path
    else:
        print('Неверный путь.')
        return get_files_path()


def copy_files(to_path, from_full_path):
    file_name = os.path.split(from_full_path)
    to_full_path = os.path.join(to_path, file_name[1])
    shutil.copy(from_full_path, to_full_path)
    print("Copy file: {0}".format(file_name[1]))
    time.sleep(random.randint(1, 5))


if __name__ == '__main__':
    # copy_files('/home/natali/py', '/home/natali/py2')
    from_name, to_name = get_files_path()
    threads_number = get_threads_number('settings.json')
    if not threads_number:
        threads_number = 3
    pool = Pool(threads_number)
    pool.map(partial(copy_files, to_name), from_name)
    pool.close()
    pool.join()
    print('Файлы успешно скопированы.')
