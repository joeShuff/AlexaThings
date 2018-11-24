import os

path = "B:\Programs\MegaSync\PD Sounds\\bain"

amount = 500

def rename():
    global amount, path
    for i in range(amount):
        try:
            os.rename(path + "\\ (" + str(i + 1) + ").wav", path + "\\" + str(i + 1) + ".wav")
            print("Renaming " + str(i + 1))
        except:
            pass

rename()