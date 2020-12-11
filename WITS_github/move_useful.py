import os
import shutil


def move_file(filename):
    os.chdir(filename)
    filelist = os.listdir()
    csv_file = ''
    for file in filelist:
        file_type = str(file).split('.')[1]
        if file_type == 'csv':
            csv_file = str(file)
    current_path = os.getcwd()
    csv_path = current_path + '/' + csv_file
    new_path = os.path.abspath(os.path.dirname(os.getcwd())) + '/csv_file/' + csv_file
    # print(csv_path)
    # print(new_path)
    shutil.copyfile(csv_path, new_path)
    os.chdir(os.path.abspath(os.path.dirname(os.getcwd())))


if __name__ == '__main__':
    path = os.getcwd()  # 获取当前路径
    count = 0
    files = os.listdir(path)
    for file in files:
        if str(file) == 'csv_file' or str(file) == '原始压缩包':
            continue
        file_type = str(file).split('.')[1]
        if file_type != 'zip_files':
            continue
        else:
            move_file(file)
            count += 1
            print(count)