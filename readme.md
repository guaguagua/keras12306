# 版本说明  
- Python       Version  3.6.8 |Anaconda, Inc.| (default, Feb 21 2019, 18:30:04) [MSC v.1916 64 bit (AMD64)]  

- tensorflow  Version  2.0.0-beta0 
  tensorflow_gpu-2.0.0b0-cp36-cp36m-win_amd64.whl 

- tf.keras       Version  2.2.4-tf  

- selenium    Version  3.141.0  

- 系统：Windows7 旗舰版  

- GPU  
  cuda_10.0.130_411.31_win10.exe  
  GTX 960   


# 网盘位置  
- 包含图片数据  

- [xxx]()

# 原始数据  
- 文件夹：originData  
  存放抓取的原始数据 ，可以用于训练和测试

# 物体识别训练  
- 文件夹：pictureTrain  
  pictureTrain文件夹下是验证码中物体识别训练，相关代码和数据  
  
- pictureTrain.py 是训练使用代码  

- mode12306_picture_class.h5 是训练完成后保存的模型数据  

- 文件夹：test 
  存放测试用图片数据，模型训练完后可以用于测试模型精度  
  
- 文件夹：train  
  存放测试图片数据  

- 文件夹：val  
  存放训练时使用的验证数据集  

# 中识别训练  
- 文件夹：chineseTrain  
  chineseTrain文件夹下是中文识别训练，相关代码和数据  
  
- chineseTrain.py 是训练使用代码  

- mode12306_chinese_class.h5 是训练完成后保存的模型数据 

- 文件夹：test  
 ./test/data 下放的是训练完成后用于测试的图片  

- 文件夹：testClass  
  - 准确度测试
   运行测试代码后，./test/data下的图片会被分类到testClass
   通过查看testClass，可以知道分类是否准确  
  - 迭代train数据  
   因为原始数据太多，手工标注太慢，可以先手工标注小部分数据 
   然后把未标注的数据放到./test/data，用新模型分类到testClass
   testClass中的大部分数据分类都是正确的
   这样可以快速迭代，新增train数据
  
- 文件夹：train  
 用于训练的数据 

- 文件夹：val  
暂时未使用，训练时val和train使用相同数据集


# 数据获取  
- 文件夹：dataGet
- 使用selenium 点击验证码刷新按钮获取验证码数据  

# flask API  
- 文件夹：flask_web
  把验证码识别作为网页形式，上传图片后返回识别结果  

- 文件夹：model
  神经网络模型  
  
- 文件夹：static 
  图片资源  

- 文件夹：templates
  HTML文档 
  
- NeuralNet.py
  神经网络模型API

- serive.py 
  flask web服务
  
# 12306自动登录  
- 文件夹：autoLogin
  自动登录