import sec_main_wits


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
        f.write("import perform_number")
        f.write("\n")
        f.write("\n")
        f.write("perform_number.perform("+str(i+1)+")")
        f.write("\n")
        f.close()


if __name__ == '__main__':
    # read_csv("/Users/graham/!Jupyter/WITS/hs_remain.csv")
    # create_success()
    # create_error()
    # create_line()
    create_perform()
    # sec_main_wits.CSV_start("test.csv", "2_error_log/error_1.txt",  "2_success_log/success_1.txt",  "line_log/linelog_1.txt")