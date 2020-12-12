from Second_Round import sec_main_wits
import os


def perform(num):
    pwd = os.getcwd()
    father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")

    csv_file = os.path.join(father_path, "csv", "csv_"+str(num)+".csv")
    error_file = os.path.join(father_path, "2_error_log", "error_"+str(num)+".txt")
    success_file = os.path.join(father_path, "2_success_log", "success_" + str(num) + ".txt")
    linelog_file = os.path.join(father_path, "line_log", "linelog_" + str(num) + ".txt")

    sec_main_wits.CSV_start(csv_file, error_file, success_file, linelog_file)
