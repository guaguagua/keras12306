from selenium import webdriver
import time
import base64
import hashlib

def getPicture():
    driver = webdriver.Chrome()

    curUrl = 'https://kyfw.12306.cn/otn/resources/login.html'
    driver.get(curUrl)
    # print(driver.current_url)
    time.sleep(1)

    # 点击帐号登录按钮
    mailLoginBUtton = driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[2]/ul[1]/li[2]")
    mailLoginBUtton.click()

    # 刷新频率太快图片
    tooFast = '''data:image/jpg;base64,/9j/4QAYRXhpZgAASUkqAAgAAAAAAAAAAAAAAP/sABFEdWNreQABAAQAAAAeAAD/7gAOQWRvYmUAZMAAAAAB/9sAhAAQCwsLDAsQDAwQFw8NDxcbFBAQFBsfFxcXFxcfHhcaGhoaFx4eIyUnJSMeLy8zMy8vQEBAQEBAQEBAQEBAQEBAAREPDxETERUSEhUUERQRFBoUFhYUGiYaGhwaGiYwIx4eHh4jMCsuJycnLis1NTAwNTVAQD9AQEBAQEBAQEBAQED/wAARCAC+ASUDASIAAhEBAxEB/8QAagABAAMBAQAAAAAAAAAAAAAAAAECAwQHAQEAAAAAAAAAAAAAAAAAAAAAEAEAAgICAQMCAgoDAAAAAAAAAQIRAyESBDFBE1EiFAVhcYGRsTJCYrIjoXIVEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwD0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHDPn7IiLdIxM39ZxxT96fx151zeKVjE1iJ7Zj7vrxGMOS81msRMdZmt5rE2iIza2J9Y94abaT03xqriK/FMR6x6e0A3nzdtbdZiluInNLTMc2iv0V/H3+HXfFIts7fzTMR9s/qc9fmjtSZzqrObTMRWM1vHOcfQmLfhdNI7Ra0TxH/fj2B1R582mIrGusYic2viOZ9uITbzb13zTpnX3jX2zz2ly1++czE5i2uOeZ4tOfaFrR28uYiZm0b6T1/tiOZB0V8vbW1qbtfS3W168+0fVnH5jedc2itYmOuImZnOYziMRKs0r88xqv3iuu8WvecxW059WPxz023i8TSl4mJr/AFTMW9P08wDsp5t51d5rWbdorNc2rjMe+aqV/MNkzeZpTFP7+ePX25U00n8PMT2mbWrF60jNo6RiYn9eGdKzbZtr/sjM/dNac88x6TxgHfbya0rHeLRaY7TitpiP24U8bzK7qVm0TF7TicVnr6/X0U8rZe+unj68/Jtj7oniYrEc/qyp4940bK4iaaN3EVt/RePb9oLa/O27NlqU1Z6xM+uPScesr+L5dt8xW1Os9e2YniecOP79Vr57UvNZikRxMza84hv4Or4tl67Jn5tcY65jrNZ5jHAO9nt2WpNIrET2ticzjj6x9TRt+bVGzrNe3tLDzsRbx7T7ba8/oBSfzDbG3p8XGM4+7P8Ag02eXam6NURTn+q18e2eY9nBNLfFN7ViJtM9Ptrzz7e//Dbf8nzxbE5rFccfSImQb6fOnbtjXisZmI/mifafT9ytPzC969orrrn2tsiJ/gw8bXeJ8eZieZzHOeIic8Y4U8W8R1ps2fFTpNs4jOe36YkHfHlXjVbZa2r7ZiPttMxz9ZiJZf8AoW7zTFOIz2zbH+GWG3vbRvrSZ2a+1IpbERn3n0jnlOyu3VsnZs7RFq4iLbIzOP4wDsjyL2ik1it+0TMxFuePTHbClvM3fJTXXVGb5x91fbmfSZYa4ik+FOyOs42ROY9pjjKum2qvw3jEY3WicfS3oDvjdM+TOnrxFO3b9uGzGJ1/iZjP+zpGYxPpmfdsAAAAAAAAAAAACDCQEYiTCQEYEgIwjrH0WARgwkBGBICMRPqYj190gIEgIMJARgSAgwkBAkBCQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB//2Q=='''
    # 验证码图片 //img[@id='J-loginImg']
    count = 0
    while_count = 0
    imageMd5List = []  # 保存已经下载了的图片，已经下载过就不下载了

    tooFast = tooFast.split(",")[-1]  # 删除前面的 “data:image/jpeg;base64,”
    tooFast = tooFast.replace("%0A", '\n')  # 将"%0A"替换为换行符
    tooFast = base64.b64decode(tooFast)  # b64decode 解码
    fmd5 = hashlib.md5(tooFast).hexdigest()

    imageMd5List.append(fmd5)  # 先把提示太快的图片 MD5值存起来
    print(imageMd5List)

    while True:
        # 点击刷新 ,#验证码刷新按钮 //div[@class='lgcode-refresh']
        driver.find_element_by_xpath("//div[@class='lgcode-refresh']").click()
        while_count += 1
        print('while_count:' + str(while_count))
        if 0 == (while_count % 3):
            # driver.get(curUrl)
            # mailLoginBUtton = driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[2]/ul[1]/li[2]")
            # mailLoginBUtton.click()
            time.sleep(10)
        else:
            time.sleep(2)

        while True:
            image = driver.find_element_by_xpath("//img[@id='J-loginImg']")
            if image.is_displayed():
                break
            print('sleep 0.5 ......')
            time.sleep(0.5)

        js = '''
        var image = document.getElementById("J-loginImg");
        var text  = image.getAttribute("src");
        //console.log(text);
        return text'''
        img_str = driver.execute_script(js)
        img_str = img_str.split(",")[-1]  # 删除前面的 “data:image/jpeg;base64,”
        img_str = img_str.replace("%0A", '\n')  # 将"%0A"替换为换行符
        img_data = base64.b64decode(img_str)  # b64decode 解码
        fmd5 = hashlib.md5(img_data).hexdigest()
        if fmd5 in imageMd5List:
            if fmd5 == imageMd5List[0]:
                print('get same fastPicture')
            else:
                print('get same picture:' + str(fmd5))
            continue

        imageMd5List.append(fmd5)
        # print(imageMd5List)
        with open('./picture/Mydownload/%s.png' % (count,), 'wb') as fout:
            fout.write(img_data)
            fout.close()
            count += 1
            print('count:' + str(count))


if __name__ == '__main__':
    getPicture()
