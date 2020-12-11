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


if __name__ == '__main__':
    read_csv("/Users/graham/!Jupyter/WITS/hs_remain.csv")