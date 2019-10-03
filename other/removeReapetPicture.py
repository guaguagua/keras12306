from PIL import Image
import glob
import os
import hashlib

def removeRepeatPicture():
    fmd5List = []
    count = 0
    errorCount = 0
    removeCount = 0
    for filename in glob.glob(r'*.png'):
        count += 1
        img = Image.open(filename)
        try:
            x = img.tobytes()
        except:
            print(filename+' tobytes error','errorCount:',errorCount)
            errorCount += 1
            #os.remove(filename)# 删除不能读数据的图
            continue            
        fmd5=hashlib.md5(x).hexdigest()
        if fmd5 in fmd5List:
            os.remove(filename)
            removeCount += 1
            print('remove repeat file '+filename + ' removeCount ' + str(removeCount))
        else:
            fmd5List.append(fmd5)
    print(count,errorCount,removeCount)

removeRepeatPicture()