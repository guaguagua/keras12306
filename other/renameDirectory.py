import shutil,os
def scandir() :
    count = 0
    for obj in os.listdir(os.curdir) :
        if os.path.isdir(obj) :
            print(obj)
            shutil.move(obj,str(count)+obj)
            count +=  1
        else:
            print('error')
scandir()            