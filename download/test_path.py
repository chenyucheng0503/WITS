# coding=utf-8
import os
"""
Author:Graham
data: 2020/10/22 0:44
"""
current_path = os.path.abspath(os.path.dirname(os.getcwd()))
success_path = current_path + "\\successlog\\success_download.txt"
print(success_path)
f = open(success_path, 'a')
