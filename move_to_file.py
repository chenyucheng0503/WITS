# coding=utf-8

"""
Author:Graham
data: 2020/12/6 11:16
"""
import os
import shutil


def move_to_file(filename, tofile):
    path = filename
    count = 0
    files = os.listdir(path)
    for file in files:
        # file_type = str(file).split('.')[1]
        if str(file)[-3:] != 'zip':
            continue
        else:
            new_path = filename + '/' + str(file)
            shutil.move(new_path, tofile)
            count += 1
            print(str(count) + " : " + str(file) + "移动成功")


if __name__ == '__main__':
    move_to_file(r"C:/Users/17313/Downloads",r"C:/Users/17313/Downloads/第二阶段/")