import os
 
def scandir(startdir) :
    os.chdir(startdir)
    for obj in os.listdir(os.curdir) :
        if os.path.isdir(obj) :
            scandir(obj)
            os.chdir(os.pardir)
        elif os.path.isfile(obj):
            os.remove(obj)
        else:
            print('error')
scandir(r'./')            