import subprocess
import os

filename = "perform_6.py"

while True:
    p = subprocess.Popen('python '+filename, shell=True).wait()
    if p != 0:
        continue
    else:
        os.system("python " + filename)
