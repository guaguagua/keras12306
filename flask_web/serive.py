from flask import Flask,request,render_template
import NeuralNet
import time
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
#neu = NeuralNet.ParsePicture()

@app.route('/', methods=['get'])
def hello():
    return render_template('index.html', chinesePredict='None', picturePredict='None')

@app.route('/upload_picture', methods=['post'])
def up_photo():
    img = request.files.get('pic')
    img.save('static/src_image.png')
    global neu
    result = NeuralNet.ParsePicture().getResult()
    #print('中文预测值', result[1])
    #print('图片预测值', result[0])
    return render_template('upload.html', chinesePredict=str(result[1]), picturePredict=str(result[0]), val1=time.time())

if __name__ == '__main__':
    app.run(debug=True)
    #http_server = WSGIServer(('127.0.0.1', 5000), app)
    #http_server.serve_forever()