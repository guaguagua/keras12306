from PIL import Image
import glob
import os
import hashlib


def deleteChinesePciture():
    for filename in glob.glob(r'*.png'):
        if '-cn' in filename:  # 删除旧的汉字剪切图片
            os.remove(filename)
            print('remove file:' + filename)


def getSmallPicture(img, number):  # 获取验证码中的8个小图
    position = [(6, 40), (78, 40), (150, 40), (220, 40), (6, 114), (78, 114), (150, 114), (220, 114)]
    # img = Image.open(filename)
    startX = position[number][0]
    startY = position[number][1]
    cutXLen = 66
    cutYLen = 66
    cropped = img.crop((startX, startY, startX + cutXLen, startY + cutYLen))  # (left, upper, right, lower)
    return cropped


def getAllSmallPicture():  # 获取验证码中的8个小图,并保存
    count = 0
    for filename in glob.glob(r'./originPicture/*.png'):
        img = Image.open(filename)
        count += 1
        print(filename, count)
        for i in range(8):
            cropped = getSmallPicture(img, i)
            fmd5 = hashlib.md5(cropped.tobytes()).hexdigest()
            newName = fmd5 + '.png'
            # print(cropped)
            cropped.save(r"./smallCutPicture/" + newName)

def getBinaryImage(img):  # 图像二值化处理
    # for filename in glob.glob(r'./chinese/*.png'):
    # print(filename)
    # img = Image.open(filename)
    Lim = img.convert('L')
    threshold = 185
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    # convert to binary image by the table
    bim = Lim.point(table, '1')
    return bim
    # filename = filename.split('\\')[-1]
    # print(filename)
    # bim.save('./binaryPNG/' + filename)


# getBinaryImage()

def getCutLine(img):  # 从x=160像素开始，如果某列的20个像素，有18个像素为白色,就是分界线,0是黑色，1是白色
    # for filename in glob.glob(r'./binaryPNG/*.png'):
    # img = Image.open(filename)
    # print('imgSize:',img.size)
    pix = img.load()
    count = 0

    # 在24-27像素的位置需要判断下，确认前面一个分类是否是 "锣" ，
    '''
    for x in range(24,28):
        count = 0
        for y in range(0,20):
            if pix[(x,y)] :
                count += 1
        if count >= 20:
            return x    
    '''
    # 在17-20像素的位置需要判断下，确认前面一个分类是否是 "锣" ，
    '''
    for x in range(17,20):
        count = 0
        for y in range(0,20):
            if pix[(x,y)] :
                count += 1
        if count >= 20:
            return x 
    '''

    for x in range(40, 60):
        count = 0
        for y in range(0, 20):
            if pix[(x, y)]:
                count += 1
        if count >= 20:
            # print(filename + ' cutLine is:',x,count)
            # break
            return x
    # print('count',count)
    return 39


# getCutLine()
def getChineseNumber(bim, firstStartX):  # 获取图片中有几个词语  1个或2个
    pix = bim.load()
    count = 0
    startX = 60
    if firstStartX < 21:
        startX = 50
    for x in range(startX, 90):
        for y in range(0, 20):
            if 0 == pix[(x, y)]:  # 在 (startX,90)之间有像素，就表示有第二个图片
                return 2
    return 1


def renamePicture(start):
    # start = 20000
    for filename in glob.glob(r'./originPicture/*.png'):
        print(filename)
        os.rename(filename, r'./originPicture/%s.png' % (start))
        start += 1
        # break
    print('rename end...')


# renamePicture()

def removeRepeatAndBadPicture():
    fmd5List = []
    count = 0
    errorCount = 0
    for filename in glob.glob(r'./originPicture/*.png'):
        # print('count:',count)
        count += 1
        img = Image.open(filename)
        try:
            x = img.tobytes()
        except:
            print(filename + ' tobytes error', 'errorCount:', errorCount)
            errorCount += 1
            os.remove(filename)  # 删除不能读数据的图
            continue
        fmd5 = hashlib.md5(x).hexdigest()
        if fmd5 in fmd5List:
            os.remove(filename)
            print('remove repeat file ' + filename)
        else:
            fmd5List.append(fmd5)
    print(count, errorCount)


# removeRepeatAndBadPicture()
# renamePicture(50000)
# renamePicture(0)

def curChinesePicture():  # 剪切中文
    # deleteChinesePciture()
    count = 0
    errorCount = 0
    for filename in glob.glob(r'./originPicture/*.png'):
        # print(filename)
        print(filename.split('.')[-2].split('\\')[-1])
        # startX=120,endX = 180
        # startY=0,endY = 28
        img = Image.open(filename)
        # print(img.size)
        try:
            cropped = img.crop((120, 4, 220, 24))  # (left, upper, right, lower)
        except:
            print(filename + ' cropped error,size:', img.size)
            errorCount += 1
            os.remove(filename)  # 删除不能读数据的图
            continue
        # print('imgSize:',cropped.size)
        count += 1
        bim = getBinaryImage(cropped)
        # bim.save('./binaryPNG/' + filename)

        x = getCutLine(bim)
        chineseNum = getChineseNumber(bim, x)
        # print(filename,x,chineseNum)
        # print('size:',img.size,'x:',x)
        # img = Image.open(filename)

        cropped0 = img.crop((120, 4, 120 + x, 24))
        cropped0 = cropped0.resize((60, 20))
        newName0 = filename.split('.')[-2].split('\\')[-1] + '-cn0' + '.' + 'png'
        cropped0.save('./chinese/' + newName0)
        if 2 == chineseNum:
            cropped1 = img.crop((120 + x, 4, 120 + x + 60, 24))
            newName1 = filename.split('.')[-2].split('\\')[-1] + '-cn1' + '.' + 'png'
            cropped1.save('./chinese/' + newName1)
            # print(filename + ' 2 chinese')
            # img.save('./two/X'+ filename)
            # bim.save('./two/' + filename)
        else:
            pass
            # print(filename + ' 1 chinese')
            # img.save('./one/X'+filename)
            # bim.save('./one/' + filename)
    print('total PASS file:', count)
    print('total FAIL file:', errorCount)


if __name__ == '__main__':
    pass
    # curChinesePicture()
    # getAllSmallPicture()
