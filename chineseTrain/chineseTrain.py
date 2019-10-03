import os
import sys
import shutil
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import optimizers
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image as kerasImage
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt


class ChineseTrain:
    def __init__(self):
        self.imageSizeX = 2 * 60 # 剪切到的原始中文图片大小是 60 *20,为了适配VGG模型，把图片放大一倍
        self.imageSizeY = 2 * 20

        self.cur_dir        = sys.path[0]
        self.train_dir      = self.cur_dir + r'\train'
        self.validation_dir = self.cur_dir + r'\train'
        print(self.cur_dir)
        print(self.train_dir)
        print(self.validation_dir)

        self.dataInit()
        self.modelInit()

    def getCountOfFile(self, startdir): # 统计某路径下的所有某种类型文件
        os.chdir(startdir)
        count = 0
        for obj in os.listdir(os.curdir):
            if os.path.isdir(obj):
                count += self.getCountOfFile(obj)
                os.chdir(os.pardir)
            elif os.path.isfile(obj):
                count += 1
            else:
                print('error')
        return count

    def dataInit(self):
        self.train_datagen   = ImageDataGenerator(rescale=1./255)
        self.val_datagen     = ImageDataGenerator(rescale=1./255)
        self.batch_size      = 20

        self.train_generator = self.train_datagen.flow_from_directory(self.train_dir,
                                                    target_size=(self.imageSizeX, self.imageSizeY),
                                                    batch_size=self.batch_size,
                                                    class_mode='categorical')

        self.validation_generator = self.val_datagen.flow_from_directory(self.validation_dir,
                                                    target_size = (self.imageSizeX,self.imageSizeY),
                                                    batch_size=self.batch_size,
                                                    class_mode='categorical')
        #train_generator.class_indices

    def modelInit(self):
        self.conv_base = VGG16(weights='imagenet', include_top=False, input_shape=(self.imageSizeX, self.imageSizeY, 3))
        self.conv_base.trainable = True
        set_trainable = False
        for layer in self.conv_base.layers:
            if layer.name == 'block5_conv1':
                set_trainable = True
            if set_trainable:
                layer.trainable = True
            else:
                layer.trainable = False

        self.model = models.Sequential()
        self.model.add(self.conv_base)
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(256,activation='relu',input_dim=3*1*512))
        self.model.add(layers.Dropout(0.5))
        self.model.add(layers.Dense(100,activation='relu'))
        self.model.add(layers.Dropout(0.5))
        self.model.add(layers.Dense(80,activation='softmax'))
        self.model.compile(optimizer=optimizers.RMSprop(lr=2e-5),
                            loss = 'categorical_crossentropy',
                            metrics=['acc'])
        self.model.summary()

    def train(self):
        count = self.getCountOfFile(self.train_dir)
        self.history = self.model.fit_generator(self.train_generator,
                                     steps_per_epoch = count/20+1,
                                     epochs = 50,
                                     validation_data = self.validation_generator,
                                     validation_steps = count/20+1)
        self.model.save(self.cur_dir+r'\mode12306_chinese_class.h5')

    def showTrian(self):
        acc      = self.history.history['acc']
        val_acc  = self.history.history['val_acc']
        loss     = self.history.history['loss']
        val_loss = self.history.history['val_loss']
        epochs   = range(1, len(acc)+1)
        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and  validation accuracy')
        plt.legend()
        plt.figure()

        plt.plot(epochs, loss, 'bo', label='Training loss')
        plt.plot(epochs, val_loss, 'b', label='Validation loss')
        plt.title('Training and  validation loss')
        plt.legend()

        plt.show()


class TestChinese:
    def __init__(self):
        self.cur_dir  = sys.path[0]
        self.test_dir = self.cur_dir + r'\test\data\\'
        self.des_dir  = self.cur_dir + r'\testClass\\'
        self.imageSizeX = 2 * 60
        self.imageSizeY = 2 * 20
        self.model = load_model('mode12306_chinese_class.h5')
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

        self.clearFold(self.des_dir)

    def clearFold(self, startdir):
        os.chdir(startdir)
        for obj in os.listdir(os.curdir):
            if os.path.isdir(obj):
                self.clearFold(obj)
                os.chdir(os.pardir)
            elif os.path.isfile(obj):
                os.remove(obj)
            else:
                print('error')

    def testTrain(self):  # 用于测试训练后分类是否准确
        count = 0
        for fileName in os.listdir(self.test_dir):
            count += 1
            if '.png' not in fileName:
                continue
            data = kerasImage.load_img(self.test_dir+fileName, target_size=(self.imageSizeX, self.imageSizeY))
            data = kerasImage.img_to_array(data)
            data = data.reshape((1,) + data.shape)
            data = data/255.0
            pre = list(self.model.predict_classes(data))
            print(count, self.class_dic_new[pre[0]])
            #print(test_dir+fileName, des_dir+class_dic_new[pre[0]]+'\\'+fileName)
            shutil.copy(self.test_dir+fileName, self.des_dir + self.class_dic_new[pre[0]] + '\\' + fileName)

''' #需要训练是打开该注释
chinese_train = ChineseTrain()
chinese_train.train()
chinese_train.showTrian()
'''

TestChinese().testTrain()









    

