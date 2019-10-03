import shutil,os
def scandir(dir,driFrom) :
    dirFromName = os.listdir(driFrom)
    print(dirFromName)
    os.chdir(dir)
    for obj in os.listdir(os.curdir) :
        if os.path.isdir(obj) :
            for copyName in dirFromName:
                if obj[-len(obj)+1:] in copyName:
                    shutil.move(obj,copyName)
            
driFrom = r'E:\Spider\Code\data\temp'
scandir(r'E:\Spider\Code\data\chinese\train',driFrom)            