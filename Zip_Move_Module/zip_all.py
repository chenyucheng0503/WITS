import os
import zipfile
import shutil


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)


def unzip_file(path):
    filenames = os.listdir(path)  # 获取目录下所有文件名
    count = 0
    for filename in filenames:
        file_str = str(filename).split('.')[0]
        file_type = str(filename).split('.')[1]
        filepath = os.path.join(path, filename)

        if file_type != 'zip':
            continue

        if len(file_str) != 18:
            shutil.move(filepath, r"C:\Users\17313\Downloads\重复文件")
            print("存在重复数据")
            continue

        try:
            zip_file = zipfile.ZipFile(filepath)  # 获取压缩文件
        except zipfile.BadZipFile:
            continue

        newfilepath = filename.split(".")[0]  # 获取压缩文件的文件名
        newfilepath = r"C:\Users\17313\Downloads\下载文件\解压后文件"

        if os.path.isdir(newfilepath):  # 根据获取的压缩文件的文件名建立相应的文件夹
            pass
        else:
            os.mkdir(newfilepath)
        for name in zip_file.namelist():  # 解压文件
            if str(name).split('.')[1] == "csv":
                try:
                    zip_file.extract(name, newfilepath)
                except zipfile.BadZipFile:
                    continue
        zip_file.close()

        if os.path.exists(filepath):  # 移动原先压缩包
            shutil.move(filepath, r"C:\Users\17313\Downloads\下载文件\原始压缩包")

        count += 1
        print(str(count) + "解压{0}成功".format(filename))


if __name__ == '__main__':
    path = r"C:\Users\17313\Downloads\第一阶段"  # 获取当前路径
    unzip_file(path)
    # for root, dirs, files in os.walk(path):  # 遍历统计
    #     for file in files:
    #         file_str = str(file).split('.')[0]
    #         file_type = str(file).split('.')[1]
    #         if file_type != 'zip':
    #             continue
    #         else:
    #             if len(file_str) != 18:
    #                 shutil.move(path + '/' + str(file), "C:/Users/17313/Downloads/第二阶段/重复数据")
    #                 print("存在重复数据")
    #             else:
    #                 un_zip(file)
    #                 count += 1
    #                 print(count)
    #     break;
