from flask import Flask, render_template, request, redirect, url_for, jsonify,Response
import cv2
import numpy as np
import io
import urllib
import urllib.parse
import urllib.request
import base64
import json
import tempfile
import os

app = Flask(__name__)

@app.route('/')  # 当用户访问根目录的时候显示的前端页面
def index():
    return render_template('index.html')  # 返回一个前端界面

@app.route('/upload', methods=['POST'])  # 进行表单请求以后进行如下操作
def upload():
    client_id = 'b6NaSaMhgzcGG1GOLMqroX4q'
    client_secret = 'Ok2iXyMKZxljVHRpu8geyNeqebrndNPh'

    def get_token():
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        token_content = response.read()
        if token_content:
            token_info = json.loads(token_content.decode("utf-8"))
            token_key = token_info['access_token']
        return token_key

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def get_license_plate(path):
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
        f = get_file_content(path)
        access_token = get_token()
        img = base64.b64encode(f)
        params = {"custom_lib": False, "image": img}
        params = urllib.parse.urlencode(params).encode('utf-8')
        request_url = request_url + "?access_token=" + access_token
        request = urllib.request.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib.request.urlopen(request)
        content = response.read()
        if content:
            license_plates = json.loads(content.decode("utf-8"))
            strover = '识别结果:'
            words_result = license_plates['words_result']
            number = words_result['number']
            strover += '  车牌号:{} \n '.format(number)
            print(strover)
            return strover  # 返回识别结果
        else:
            return ''
    image = request.files['file']
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    image.save(temp_file.name)
    temp_file.close()

    result = get_license_plate(temp_file.name)
    os.unlink(temp_file.name)

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
    # app.run()
