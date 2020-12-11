import os
import main_wits


def get_hs(num):
    current_path = os.getcwd()
    parent_path = os.path.abspath(os.path.dirname(os.getcwd()))
    HS_path = parent_path + "/HS_cut/HS" + str(num) + ".txt"
    f = open(HS_path)
    lines = f.readlines()
    f.close()
    # 加载error和success路径
    error_path = parent_path + "/errorlog/error" + str(num) + ".txt"
    success_path = parent_path + "/successlog/success" + str(num) + ".txt"
    for line in lines:
        line = int(line[:-1])
        main_wits.HS_start(HS_Code=int(line), error_log=error_path, success_log=success_path)

