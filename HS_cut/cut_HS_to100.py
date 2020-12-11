# 将所有代码分成100份方便多线程

f = open('HS.txt', 'r').readlines()
n = 100  # 份数
qty = len(f)//n if len(f)%n==0 else len(f)//n+1  # 每一份的行数
for i in range(n):
    a = open('HS_cut/HS' + str(i+1) + '.txt', 'a')
    a.writelines(f[i*qty:(i+1)*qty])
    a.close()
    print("finish" + str(i))

