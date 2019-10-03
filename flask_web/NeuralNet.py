import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import optimizers
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import VGG16
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image as kerasImage
from keras.callbacks import LambdaCallback

import numpy as np
import shutil
import base64
import hashlib
from PIL import Image

import random
import sys
import time
import os

print("Python     Version {}".format(str(sys.version).replace('\n', '')))
print('tensorflow Version ', tf.__version__)
print('tf.keras   Version ', keras.__version__)


class ParsePicture:
    def __init__(self):
        self.class_dic = {'中国结': 0, '仪表盘': 1, '公交卡': 2, '冰箱': 3, '创可贴': 4, '刺绣': 5, '剪纸': 6, '印章': 7, '卷尺': 8,
                          '双面胶': 9, '口哨': 10, '啤酒': 11, '安全帽': 12, '开瓶器': 13, '手掌印': 14, '打字机': 15, '护腕': 16,
                          '拖把': 17, '挂钟': 18, '排风机': 19, '文具盒': 20, '日历': 21, '本子': 22, '档案袋': 23, '棉棒': 24,
                          '樱桃': 25, '毛线': 26, '沙包': 27, '沙拉': 28, '海报': 29, '海苔': 30, '海鸥': 31, '漏斗': 32,
                          '烛台': 33, '热水袋': 34, '牌坊': 35, '狮子': 36, '珊瑚': 37, '电子秤': 38, '电线': 39, '电饭煲': 40,
                          '盘子': 41, '篮球': 42, '红枣': 43, '红豆': 44, '红酒': 45, '绿豆': 46, '网球拍': 47, '老虎': 48,
                          '耳塞': 49, '航母': 50, '苍蝇拍': 51, '茶几': 52, '茶盅': 53, '药': 54, '菠萝': 55, '蒸笼': 56,
                          '薯条': 57, '蚂蚁': 58, '蜜蜂': 59, '蜡烛': 60, '蜥蜴': 61, '订书机': 62, '话梅': 63, '调色板': 64,
                          '跑步机': 65, '路灯': 66, '辣椒酱': 67, '金字塔': 68, '钟表': 69, '铃铛': 70, '锅铲': 71, '锣': 72,
                          '锦旗': 73, '雨靴': 74, '鞭炮': 75, '风铃': 76, '高压锅': 77, '黑板': 78, '龙舟': 79}

        self.class_dic_new = {value: key for key, value in self.class_dic.items()}

        self.smallImageSizeX = 66        # 验证码一张小图片长度大小
        self.smallImageSizeY = 66        # 验证码一张小图片高度大小
        self.chineseImageX   = 2*60      # 验证码一张中文图片长度大小
        self.chineseImageY   = 2*20      # 验证码一张中文图片高度大小

        self.modelPicture = load_model(r'model/mode12306_picture_class.h5')  # 加载图片预测模型
        self.modelChinese = load_model(r'model/mode12306_chinese_class.h5')  # 加载中文预测模型

    def predictPicture(self, img, num):  # image = 分割后的小图片
        img.save(r"static/picture_image%s.png" % (num,))
        data = kerasImage.load_img('static/picture_image%s.png' % (num,), target_size=(self.smallImageSizeX, self.smallImageSizeY))
        data = kerasImage.img_to_array(data)
        data = data.reshape((1,) + data.shape)
        data = data / 255.0

        pre = list(self.modelPicture.predict_classes(data))
        return pre[0]  # 返回图片的分类

    def predictChinese(self, img, num):
        img.save(r"static/chinese_image%s.png" % (num,))
        data = kerasImage.load_img('static/chinese_image%s.png' % (num,), target_size=(self.chineseImageX, self.chineseImageY))
        data = kerasImage.img_to_array(data)
        data = data.reshape((1,) + data.shape)
        data = data / 255.0

        pre = list(self.modelChinese.predict_classes(data))
        return pre[0]  # 返回中文的分类

    def getCutLine(self, img):
        '''
        img=剪切后的中文图片
        从x=40像素开始，如果某列的20个像素，有18个像素为白色,就是分界线,0是黑色，1是白色
        '''
        pix = img.load()
        count = 0

        for x in range(40, 60):
            count = 0
            for y in range(0, 20):
                if pix[(x, y)]:
                    count += 1
            if count >= 20:
                return x
        return 39  # 返回分割位置

    def getBinaryImage(self, img):  # img=剪切后的中文图片,图像二值化处理
        Lim = img.convert('L')
        threshold = 185
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        bim = Lim.point(table, '1')
        return bim  # 返回二值化处理后的图片

    def getChineseNumber(self, bim, firstStartX):  # bim=二值化处理后的图片,获取图片中有几个词语  1个或2个
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

    def getChinesePicture(self, img):  # 获取中文，img=验证码原始图片
        imageList = []
        try:
            cropped = img.crop((120, 4, 220, 24))  # 从验证码原始图片中，把中文部分切割出来 (left, upper, right, lower)
        except:
            print('getChinesePicture error...')
            return []

        bim = self.getBinaryImage(cropped)  # 把切割得到的中文图片进行二值化处理

        x = self.getCutLine(bim)  # 通过二值化处理后的图片，得到不同词语之间的分割线
        chineseNum = self.getChineseNumber(bim, x)  # 通过二值化处理后的图片，得到词语的个数(1个或2个)

        cropped0 = img.crop((120, 4, 120 + x, 24))  # 从验证码原始图片中，切割第一个词语
        cropped0 = cropped0.resize(
            (self.chineseImageX, self.chineseImageY))  # 改变图片大小为 (self.chineseImageX,self.chineseImageY)
        imageList.append(cropped0)

        if 2 == chineseNum:
            cropped1 = img.crop((120 + x, 4, 120 + x + 60, 24))  # 如果有两个词语，切割第二个词语
            cropped1 = cropped1.resize((self.chineseImageX, self.chineseImageY)) #
            imageList.append(cropped1)

        return imageList  # 返回中文词语列表

    def getSmallPicture(self, img):  # 获取验证码中的8个小图，img=验证码原始图片
        position = [(6, 40), (78, 40), (150, 40), (220, 40), (6, 114), (78, 114), (150, 114),
                    (220, 114)]  # 8个小图片在验证码中的位置
        imageList = []
        for number in range(8):
            startX = position[number][0]
            startY = position[number][1]
            try:
                cropped = img.crop((startX, startY, startX + self.smallImageSizeX,
                                    startY + self.smallImageSizeY))  # (left, upper, right, lower)
                imageList.append(cropped)
            except:
                print("getSmallPicture error...")
                return []
        return imageList  # 返回验证码中的8个小图片

    def getOriginPicture(self):  # 获取base64格式的验证码图片数据
        img_data = Image.open('static/src_image.png')
        return img_data

    def getResult(self):
        img_data = self.getOriginPicture()
        #print('图片预测值:')
        eight_img = self.getSmallPicture(img_data)
        imgClassList = []
        count = 0
        for img in eight_img:
            #print(self.class_dic_new[self.predictPicture(img)])
            #imgClassList.append(self.predictPicture(img))
            imgClassList.append(self.class_dic_new[self.predictPicture(img, count)])
            count += 1

        #print('中文预测值:')
        chinese_img = self.getChinesePicture(img_data)
        chineseClassList = []
        count = 0
        for img in chinese_img:
            #print(self.class_dic_new[self.predictChinese(img)])
            #chineseClassList.append(self.predictChinese(img))
            chineseClassList.append(self.class_dic_new[self.predictChinese(img, count)])
            count += 1

        clickPosList = []
        #print(imgClassList)
        #print(chineseClassList)
        for i in range(len(imgClassList)):# 查找点击位置
            if imgClassList[i] in chineseClassList:
                clickPosList.append(i)
        #print(clickPosList)
        #return clickPosList
        return [imgClassList,chineseClassList]

if __name__ == '__main__':
    ParsePicture().getResult()