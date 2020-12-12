from Second_Round import sec_main_wits
import os


def read_csv(csv_path):
    count = len(open(csv_path, 'r').readlines())
    with open(csv_path, 'r') as f:
        for i in range(count):
            if i > 5:
                break
            if i == 0:
                f.readline()
                continue
            else:
                csv_str = f.readline()
                hs_code = csv_str.split(',')[1].zfill(6)
                year = csv_str.split(',')[2]
                flow = csv_str.split(',')[3]
                print(hs_code, year, flow, end='')


def create_success():
    for i in range(10):
        f = open("success_" + str(i+1) + ".txt", "wb")


def create_error():
    for i in range(10):
        f = open("error_" + str(i+1) + ".txt", "wb")


def create_line():
    for i in range(10):
        f = open("linelog_" + str(i+1) + ".txt", "w")
        f.write("0")
        f.close()


def create_perform():
    for i in range(10):
        f = open("perform_" + str(i+1) + ".py", "w")
        f.write("from Second_Round.csv_perform import perform_number")
        f.write("\n")
        f.write("\n")
        f.write("perform_number.perform("+str(i+1)+")")
        f.write("\n")
        f.close()


def create_judge():
    for i in range(10):
        f = open("judge_" + str(i+1) + ".py", "w")
        f.write("import subprocess\n")
        f.write("import os\n")
        f.write("\n")
        f.write('filename = "perform_' + str(i+1) + '.py"\n')
        f.write("\n")
        f.write("while True:\n")
        f.write("    p = subprocess.Popen('python '+filename, shell=True).wait()\n")
        f.write("    if p != 0:\n")
        f.write("        continue\n")
        f.write("    else:\n")
        f.write('        os.system("python " + filename)\n')
        f.close()


if __name__ == '__main__':
    # read_csv("/Users/graham/!Jupyter/WITS/hs_remain.csv")
    # create_success()
    # create_error()
    # create_line()
    # create_perform()
    # create_judge()

    path = os.getcwd()
    csv_file = os.path.join(path, "csv", "csv_1.csv")
    error_file = os.path.join(path, "2_error_log", "error_1.txt")
    success_file = os.path.join(path, "2_success_log", "success_1.txt")
    linelog_file = os.path.join(path, "line_log", "linelog_1.txt")
    sec_main_wits.CSV_start(csv_file, error_file, success_file, linelog_file)