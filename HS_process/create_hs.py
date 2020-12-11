for i in range(100):
    f = open("hs"+ str(i+1) + ".py", "a+")
    f.write("from WITS import HS_loop")
    f.write("\n")
    f.write("\n")
    f.write("HS_loop.get_hs(" + str(i+1) + ")")
    f.close()

