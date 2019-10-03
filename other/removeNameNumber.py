import shutil,os
numberList = ['0','1','2','3','4','5','6','7','8','9']

def scandir() :
    for dirName in os.listdir(os.curdir) :
        print(dirName)
        i = 0
        if os.path.isdir(dirName) :
            for char in dirName:
                if char not in numberList:
                    newName = dirName[i:]
                    break
                i += 1
            shutil.move(dirName,newName)
        else:
            print('not dir '+dirName)
scandir()            