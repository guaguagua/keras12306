import os,shutil
 
def scandir(startdir) :
    os.chdir(startdir)
    for dir1 in os.listdir(os.curdir) :
        if os.path.isdir(dir1) :
            os.chdir(startdir+dir1)
            os.mkdir('data')
            for obj2 in os.listdir(os.curdir):
                if os.path.isdir(obj2) :
                    continue
                src = startdir+dir1+r'\\'+obj2
                dst = startdir+dir1+r'\\data\\'+obj2
                shutil.move(src,dst)
            os.chdir(os.pardir)
        else:
            print('error')
scandir(r'E:\Spider\Code\data\picture\test\\')            