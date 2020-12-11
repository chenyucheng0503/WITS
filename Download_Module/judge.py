import subprocess
import os

filename = "download_hs_no_delete.py"
current_path = os.getcwd()
page_log = current_path + "/page_log.txt"
f = open(page_log, 'r')
page = int(f.read())
print(page)

while page < 7642:
    p = subprocess.Popen('python '+filename, shell=True).wait()

    if p != 0:
        continue
    else:
        os.system("python " + filename)
