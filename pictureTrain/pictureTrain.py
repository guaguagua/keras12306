import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import optimizers
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import VGG16
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import LambdaCallback
import os,sys
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)
print(keras.__version__)

class PictureTrain:
    def __init__(self):
        self.imageSizeX = 66
        self.imageSizeY = 66

        self.cur_dir        = sys.path[0]
        self.train_dir      = self.cur_dir + r'\train'
        self.validation_dir = self.cur_dir + r'\val'
        print(self.cur_dir)
        print(self.train_dir)
        print(self.validation_dir)

        self.dataInit()
        self.modelInit()

    # 统计某路径下的所有某种类型文件
    def getCountOfFile(self, startdir):
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
                                                    target_size = (self.imageSizeX, self.imageSizeY),
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
        self.model.add(layers.Dense(256, activation='relu', input_dim=2*2*512))
        self.model.add(layers.Dropout(0.5))
        self.model.add(layers.Dense(80, activation='softmax'))
        self.model.compile(optimizer=optimizers.RMSprop(lr=2e-5),
                     loss = 'categorical_crossentropy',
                     metrics=['acc'])
        #self.model.summary()

    def train(self):
        self.history = self.model.fit_generator(self.train_generator,
                                  steps_per_epoch=self.getCountOfFile(self.train_dir) / self.batch_size,
                                  epochs=30,
                                  validation_data=self.validation_generator,
                                  validation_steps=self.getCountOfFile(self.validation_dir) / self.batch_size)
        self.model.save(self.cur_dir + r'\mode12306_picture_class.h5')

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




picture_train = PictureTrain()
picture_train.train()
picture_train.showTrian()