# coding=utf-8

"""
Author:Graham
data: 2020/12/8 17:12
"""
import numpy as np
import pandas as pd
import os
import shutil


def search(path, word):
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and word in filename:
            shutil.copy(fp, r"C:\Users\17313\Downloads\2018NeedPDF")
            print(filename + "已经找到")
        elif os.path.isdir(fp):
            search(fp, word)


if __name__ == '__main__':
    NeedToCSV = pd.read_csv('Need2018.csv')
    stockList = NeedToCSV['股票代码']
    for i in stockList:
        search(r"C:\Users\17313\Downloads\2017年A股上市公司年报PDF\所有压缩包", "2018-" + str(i).zfill(6) + "-")
        NeedToCSV.drop(NeedToCSV[NeedToCSV['股票代码'] == i].index, inplace=True)

    NeedToCSV.to_csv('Need2017.csv')


