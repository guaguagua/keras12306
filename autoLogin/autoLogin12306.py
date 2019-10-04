import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

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
print('selenium   Version ', selenium.__version__)


class Base12306:
    def __init__(self):
        pass

    def waitEleDisplay(self, eleXpath, timeOut=0.5):
        if timeOut <= 0.5:
            timeOut = 0.5

        element = None
        while timeOut >= 0:  # 等待显示验证码图片
            element = self.driver.find_element_by_xpath(eleXpath)
            if element.is_displayed():
                break
            print('sleep 0.5 .....waitEleDisplay:%s' % (eleXpath,))
            time.sleep(0.5)
            timeOut -= 0.5
        return element

    def waitUrlDisplay(self, url, timeOut=0.5):
        if timeOut <= 0.5:
            timeOut = 0.5

        while timeOut >= 0:
            if self.driver.current_url == url:
                break
            print('sleep 0.5 .....waitUrlDisplay:%s' % (url,))
            print(self.driver.current_url)
            time.sleep(0.5)
            timeOut -= 0.5


class Login12306(Base12306):
    def __init__(self, drive, account, password):
        self.driver = drive  # webdriver.Chrome()
        self.driver.maximize_window()
        #print(self.driver.get_window_size())
        #print(self.driver.get_window_position())

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
        self.path = os.path.split(os.path.realpath(__file__))[0]  # E:\Spider\gitHub\autoLogin
        print(self.path + r'\model\mode12306_picture_class.h5')
        self.modelPicture = load_model(self.path + r'\model\mode12306_picture_class.h5')  # 加载图片预测模型
        self.modelChinese = load_model(self.path + r'\model\mode12306_chinese_class.h5')  # 加载中文预测模型

        self.LogUrl = 'https://kyfw.12306.cn/otn/resources/login.html'  # 登录页面
        self.LogPassUrl = 'https://kyfw.12306.cn/otn/view/index.html'  # 登录成功后页面
        self.account = account  # 帐号
        self.password = password  # 密码
        self.smallImageSizeX = 66  # 验证码一张小图片长度大小
        self.smallImageSizeY = 66  # 验证码一张小图片高度大小
        self.chineseImageX = 2 * 60  # 验证码一张中文图片长度大小
        self.chineseImageY = 2 * 20  # 验证码一张中文图片高度大小

        self.loginQrXpath = "//img[@id='J-qrImg']"  # 扫描登录二维码 xPath
        self.accountLogButtonXpath = "//li[@class='login-hd-account']//a"  # 帐号登录选择按钮 xPath，选择使用帐号方式登录
        self.accountInputXpath = "//input[@id='J-userName']"  # 帐号输入框 xPath
        self.passwordInputXpath = "//input[@id='J-password']"  # 密码输入框 xPath
        self.loginButtonXpath = "//a[@id='J-login']"  # 登录按钮 xPath
        self.verifyPictureXpath = "//img[@id='J-loginImg']"  # 验证码图片 xPath

    def predictPicture(self, img):  # image = 分割后的小图片
        img.save(r"picture_image.png")
        data = kerasImage.load_img('picture_image.png', target_size=(self.smallImageSizeX, self.smallImageSizeY))
        data = kerasImage.img_to_array(data)
        data = data.reshape((1,) + data.shape)
        data = data / 255.0

        pre = list(self.modelPicture.predict_classes(data))
        return pre[0]  # 返回图片的分类

    def predictChinese(self, img):
        img.save(r"chinese_image.png")
        data = kerasImage.load_img('chinese_image.png', target_size=(self.chineseImageX, self.chineseImageY))
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
            cropped1 = cropped1.resize((imageSizeX, imageSizeY))
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
        js = '''
        var image = document.getElementById("J-loginImg");
        var text  = image.getAttribute("src");
        //console.log(text);
        return text'''
        img_str = self.driver.execute_script(js)
        img_str = img_str.split(",")[-1]  # 删除前面的 “data:image/jpeg;base64,”
        img_str = img_str.replace("%0A", '\n')  # 将"%0A"替换为换行符
        img_data = base64.b64decode(img_str)  # b64decode 解码

        return img_data

    def clickPicture(self):  # 点击验证码图片
        imgLoginEle = self.waitEleDisplay(self.verifyPictureXpath, 10)  # 等待验证码图片显示

        img_data = self.getOriginPicture()

        with open('src_image.png', 'wb') as fout:
            fout.write(img_data)
            fout.close()
        img_data = Image.open('src_image.png')

        print('图片预测值:')
        eight_img = self.getSmallPicture(img_data)
        imgClassList = []
        for img in eight_img:
            print(self.class_dic_new[self.predictPicture(img)])
            imgClassList.append(self.predictPicture(img))

        print('中文预测值:')
        chinese_img = self.getChinesePicture(img_data)
        chineseClassList = []
        for img in chinese_img:
            print(self.class_dic_new[self.predictChinese(img)])
            chineseClassList.append(self.predictChinese(img))

        clickPosList = []
        print(imgClassList)
        print(chineseClassList)
        for i in range(len(imgClassList)):  # 查找点击位置
            if imgClassList[i] in chineseClassList:
                clickPosList.append(i)

        posOffsetList = [(34, 76), (115, 76), (182, 76), (258, 76),
                         (34, 149), (115, 149), (182, 149), (258, 149)]
        print(clickPosList)

        if len(clickPosList) <= 0:
            return False

        for pos in clickPosList:
            offsetX = posOffsetList[pos][0] + random.randint(-2, 2)  # 点击位置加入一些噪声
            offsetY = posOffsetList[pos][1] + random.randint(-2, 2)
            actionChains = ActionChains(self.driver)
            actionChains.move_to_element_with_offset(imgLoginEle, offsetX, offsetY).click().perform()
            # imgLoginEle.click()
        return True

    def login(self):  # 自动登录
        self.driver.get(self.LogUrl)

        self.waitUrlDisplay(self.LogUrl, 10)  # 等待网址正确加载
        self.waitEleDisplay(self.loginQrXpath, 10)  # id="J-qrImg" 等待二维码显示

        # 点击帐号登录按钮 self.accountLogButtonXpath = "//li[@class='login-hd-account']//a"
        mailLoginBUtton = self.driver.find_element_by_xpath(self.accountLogButtonXpath)
        mailLoginBUtton.click()

        # 输入帐号 self.accountInputXpath = "//input[@id='J-userName']" #帐号输入框 xPath
        usrNameInput = self.driver.find_element_by_xpath(self.accountInputXpath)
        usrNameInput.send_keys(self.account)

        # 输入密码 id=J-password
        usrPassword = self.driver.find_element_by_xpath(self.passwordInputXpath)
        usrPassword.send_keys(self.password)

        # 点击验证码
        if not self.clickPicture():
            print('login Fail...')
            return

        # time.sleep(5)

        # 点击立即登陆  id="J-login"
        loginEle = self.driver.find_element_by_xpath(self.loginButtonXpath)
        loginEle.click()

        # 登录成功后网页 https://kyfw.12306.cn/otn/view/index.html
        self.waitUrlDisplay(self.LogPassUrl, 10)
        print(self.driver.current_url)


class BuyTicket(Base12306):
    def __init__(self, driver, name, fromStation, toStation, date, trainNumber, level):
        self.driver = driver
        self.name = name  # 乘客名字
        self.fromStation = fromStation  # '成都东'
        self.toStation = toStation  # '峨眉'
        self.date = date  # '2019-09-22'
        self.trainNumber = trainNumber  # 'C6303'
        self.level = level  # '二等座'
        self.queryUrl = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'  # 查票网址
        self.levelList = ['商务座', '一等座', '二等座', '高级软卧', '软卧一等座', '动卧', '硬卧二等座', '软卧', '硬卧', '无座', '其他']
        self.ticketTypeList = ['成人票', '儿童票', '学生票', '残军票']

        self.queryTrain()

        self.validDateList = self.getAllValidDate()

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')][1]")))
        except:
            print('timeout in __init__...')
            return

        self.validTrainList = self.getAllValidTrain()
        self.startTimeList = self.getAllValidStartTime()
        self.endTimeList = self.getAllValidEndTime()
        self.ticketNumDic = {}
        for level in self.levelList:
            self.ticketNumDic[level] = self.getTicketNumbers(level)

        self.trainAttribute = {}
        self.zipTrainData()
        # self.printTrainInfo()

    def zipTrainData(self):  #
        trainNumber = len(self.validTrainList)
        for i in range(trainNumber):
            tempDic = {}
            tempDic['startTime'] = self.startTimeList[i]
            tempDic['endTime'] = self.endTimeList[i]
            for level in self.levelList:
                ticketNumList = self.ticketNumDic[level]
                tempDic[level] = ticketNumList[i]
            self.trainAttribute[self.validTrainList[i]] = tempDic

    def printTrainInfo(self):
        for train in self.validTrainList:
            print('*' * 50)
            print('train:' + train)
            print('startTime:' + self.trainAttribute[train]['startTime'])
            print('endTime:' + self.trainAttribute[train]['endTime'])
            for level in self.levelList:
                print(level + ':' + self.trainAttribute[train][level])

    def queryTrain(self):
        js = 'window.open("%s");' % (self.queryUrl,)
        self.driver.execute_script(js)
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        self.waitUrlDisplay(self.queryUrl, 10)

        try:  # 等待查询按钮出现 self.driver.find_element_by_id('query_ticket').click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "query_ticket")))
        except:
            print('timeout in queryTrain...')
            return

        # 起始站查询 id=//input[@id='fromStationText']
        self.driver.find_element_by_id('fromStationText').click()
        self.driver.find_element_by_id('fromStationText').send_keys(self.fromStation)
        self.driver.find_element_by_id('fromStationText').send_keys(Keys.ENTER)

        # 终止站查询 id=//input[@id='toStationText']
        self.driver.find_element_by_id('toStationText').click()
        self.driver.find_element_by_id('toStationText').send_keys(self.toStation)
        self.driver.find_element_by_id('toStationText').send_keys(Keys.ENTER)

        # 选择时间  //input[@id='train_date']
        js = "document.getElementById('train_date').removeAttribute('readonly')"
        self.driver.execute_script(js)  # 移除时间选择框的readonly属性
        dateInput = self.driver.find_element_by_id('train_date')
        js = "arguments[0].value = '%s';" % (self.date,)
        self.driver.execute_script(js, dateInput)

        # 开始查询 //a[@id='query_ticket']
        self.driver.find_element_by_id('query_ticket').click()

    def getAllValidDate(self):  # 获取所有能买票的日期
        # 合法日期列表 //div[@id='date_range']//li

        self.waitUrlDisplay(self.queryUrl, 10)  # curUrl:用于判断调用函数时,是否处在正确的页面

        dateListElement = driver.find_elements_by_xpath("//div[@id='date_range']//li/span[2]")
        dateList = []
        # print(len(dateList))
        for date in dateListElement:
            dateText = date.get_attribute('textContent')
            dateText = dateText.strip().split()[0]
            dateList.append(dateText)  # https://blog.csdn.net/vinson0526/article/details/51830650

        # print(dateList)
        '''
        ['09-28', '09-29', '09-30', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', 
         '10-07', '10-08', '10-09', '10-10', '10-11', '10-12', '10-13', '10-14', '10-15', 
         '10-16', '10-17', '10-18', '10-19', '10-20', '10-21', '10-22', '10-23', '10-24', 
         '10-25', '10-26', '10-27']
        '''
        return dateList

    def getAllValidTrain(self):  # 获取所有合法的车次
        # 列车 每一行 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]
        # 列车 第一列 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]//a[@class='number']

        self.waitUrlDisplay(self.queryUrl, 10)  # curUrl:用于判断调用函数时,是否处在正确的页面

        trainNumberListElement = self.driver.find_elements_by_xpath(
            "//div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]//a[@class='number']")
        # print(len(trainNumberListElement))
        trainNumberList = []
        for number in trainNumberListElement:
            numberText = number.get_attribute('textContent')
            trainNumberList.append(numberText)
        # print(trainNumberList,len(trainNumberList))
        '''
        ['C6253', 'C6257', 'C6301', 'C6303', 'D4109', 'C6305', 'C6271', 'D4107', 'C6313', 'C6309', 'C6281', 'G8681', 'K985'] 13
        '''
        return trainNumberList

    def getAllValidStartTime(self):  # 获取每个车次的出发时间
        # 每个车次的开始时间 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]//strong[@class='start-t']

        self.waitUrlDisplay(self.queryUrl, 10)  # curUrl:用于判断调用函数时,是否处在正确的页面

        startTimeListElement = self.driver.find_elements_by_xpath(
            "//div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]//strong[@class='start-t']")
        # print(len(startTimeListElement))
        startTimeList = []
        for time in startTimeListElement:
            timeText = time.get_attribute('textContent')
            startTimeList.append(timeText)

        # print(startTimeList,len(startTimeList))
        '''['06:18', '07:18', '09:39', '11:00', '12:12', '12:32', '14:55', '15:53', '16:25', '17:12', '19:20', '20:59', '-----'] 13'''
        return startTimeList

    def getAllValidEndTime(self):  # 获取每个车次的结束时间
        # 每个车次的开始时间 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]//strong[@class='start-t']/../strong[2]

        self.waitUrlDisplay(self.queryUrl, 10)  # curUrl:用于判断调用函数时,是否处在正确的页面

        endTimeListElement = self.driver.find_elements_by_xpath(
            "//div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]//strong[@class='start-t']/../strong[2]")
        # print(len(endTimeListElement))
        endTimeList = []
        for time in endTimeListElement:
            timeText = time.get_attribute('textContent')
            endTimeList.append(timeText)

        # print(endTimeList,len(endTimeList))
        '''['07:27', '08:30', '11:13', '12:05', '13:26', '13:53', '16:29', '17:04', '17:46', '18:42', '20:36', '22:15', '-----'] 13'''
        return endTimeList

    def getTicketNumbers(self, level):
        # 每个车次的剩余票数
        # 商务座 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[2]
        # 一等座 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[3]
        # 二等座 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[4]
        # 高级软卧 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[5]
        # 软卧一等座 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[6]
        # 动卧 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[7]
        # 硬卧二等座 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[8]
        # 软卧 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[9]
        # 硬卧 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[10]
        # 无座 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[11]
        # 其他 //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[12]

        self.waitUrlDisplay(self.queryUrl, 10)  # curUrl:用于判断调用函数时,是否处在正确的页面

        # self.levelList = ['商务座','一等座','二等座','高级软卧','软卧一等座','硬卧二等座','软卧','硬卧','无座','其他']
        # print(self.levelList.index(level)+2)
        xpath = "//div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[%s]" % (self.levelList.index(level) + 2,)
        # print(xpath)
        ticketNumberElement = self.driver.find_elements_by_xpath(xpath)
        # print(len(ticketNumberElement))
        numberList = []
        for number in ticketNumberElement:
            numberText = number.get_attribute('textContent')
            numberList.append(numberText)
        # print(numberList)
        '''['有', '有', '候补', '有', '候补', '有', '有', '候补', '有', '有', '候补', '有', '--']'''
        return numberList

    def bookTicket(self):  # 点击预订按钮
        # //div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[13]

        self.waitUrlDisplay(self.queryUrl, 10)  # curUrl:用于判断调用函数时,是否处在正确的页面

        bookElementList = self.driver.find_elements_by_xpath(
            "//div[@id='t-list']//tbody[1]/tr[contains(@id,'ticket_')]/td[13]")
        # trainNumberList = self.getAllValidTrain()
        if self.trainNumber in self.validTrainList:
            index = self.validTrainList.index(self.trainNumber)
            bookElementList[index].click()
        else:
            print('没有该车次')

    def getAllPerson(self):
        # 乘车人checkbox选择 //ul[@id='normal_passenger_id']/li/label

        curUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        self.waitUrlDisplay(curUrl, 10)  # curUrl:用于判断调用函数时,是否处在正确的页面

        personElementList = self.driver.find_elements_by_xpath("//ul[@id='normal_passenger_id']/li/label")
        personList = []
        for person in personElementList:
            personText = person.get_attribute('textContent')
            personList.append(personText)
        # print(personList)
        '''['name', 'name', 'name', 'name', 'name', 'name', 'name', 'name', 'name', 'name', 'name', 'name', 'name']'''
        return personList

    def isPersonValid(self, name):  # 判断乘客是否能买票
        # //ul[@id='normal_passenger_id']/li[2]/label

        curUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        self.waitUrlDisplay(curUrl, 10)  # curUrl:用于判断调用函数时,是否处在正确的页面

        personList = self.getAllPerson()
        if name not in personList:
            return False
        index = personList.index(name)
        # print(index)
        xpath = "//ul[@id='normal_passenger_id']/li[%s]/label" % (index + 1,)
        # print(xpath)
        personElementList = self.driver.find_element_by_xpath(xpath)
        # print(personElementList.get_attribute('disabled'))
        if personElementList.get_attribute('disabled'):
            return False
        else:
            return True

    def selectPerson(self, name):
        # 乘车人checkbox选择 //ul[@id='normal_passenger_id']/li/input

        curUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        self.waitUrlDisplay(curUrl, 10)  # curUrl:用于判断调用函数时,是否处在正确的页面

        personCheckboxList = self.driver.find_elements_by_xpath("//ul[@id='normal_passenger_id']/li/input")
        personList = self.getAllPerson()
        if name in personList and self.isPersonValid(name):  # 还需要判断乘客是否能被选中,因为有些乘客的信息过时了不能买票
            index = personList.index(name)
            if not personCheckboxList[index].is_selected():  # 判断checkbox是否被选中,没有选中才选
                personCheckboxList[index].click()
            print(name + " 乘客被选中")
            return True
        else:
            print(name + ' 乘客不存在 或 不能买票')
            return False

    def selectTicketType(self, ticketType):  # 选择票的种类
        # //select[@id='ticketType_1']
        # self.ticketTypeList  #['成人票','儿童票','学生票','残军票']
        # selectByValue
        Select(self.driver.find_elements_by_xpath("//select[@id='ticketType_1']")).select_by_value(ticketType)

    def selectLevel(self, level):  # //select[@id='seatType_1']
        Select(self.driver.find_elements_by_xpath("//select[@id='seatType_1']")).select_by_value(level)

    def submitOrder(self):  # 提交订单按钮
        # curUrl:用于判断调用函数时,是否处在正确的页面
        curUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        self.waitUrlDisplay(curUrl, 10)  # curUrl:用于判断调用函数时,是否处在正确的页面

        print(self.name)
        self.selectPerson(self.name)
        self.selectTicketType('儿童票')
        # self.selectLevel()

        return
        self.driver.find_element_by_xpath("//a[@id='submitOrder_id']").click()  # 确认乘车信息

        # qr_submit_id
        self.driver.find_element_by_xpath("//a[@id='qr_submit_id']").click()  # 确认买单

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.implicitly_wait(20)
    Login12306(driver, 'account', 'password').login()

    '''
    buyTicker = BuyTicket(driver,'name','成都南','峨眉','2019-10-05','C6257','二等座')
    buyTicker.bookTicket()
    buyTicker.submitOrder()

    #buyTicker.queryTrain()
    #buyTicker.getAllValidDate()
    #buyTicker.getAllValidTrain()
    #buyTicker.getAllValidStartTime()
    #buyTicker.getAllValidEndTime()
    #buyTicker.getTicketNumbers('二等座')
    #buyTicker.bookTicket('C6303','二等座')
    #buyTicker.getAllPerson()
    #print(buyTicker.isPersonValid("name"))
    #print(buyTicker.isPersonValid("name"))
    #buyTicker.selectPerson('name')
    #buyTicker.submitOrder()
    '''