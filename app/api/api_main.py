import os
import subprocess
from werkzeug.datastructures import FileStorage
import logging
import requests
from flask import Blueprint,Response

from app.models.model import Camera
from app.utils.core import db
from flask import request
from app.utils.response import ResMsg
from app.utils.util import route
from app.utils.code import ResponseCode
import cv2
import time



bp = Blueprint("main", __name__, url_prefix='/main')

logger = logging.getLogger(__name__)

@route(bp, '/upload', methods=["POST"])
def upload():
    res = ResMsg()
    res.update(code=ResponseCode.InvalidParameter)
    if 'file' in request.files:
        file = request.files['file']
        data=dict(file=file)
        res.update(code=ResponseCode.Success,data=data)
    return res.data
@route(bp, '/process', methods=["GET"])
def process():
    res = ResMsg()
    res.update(code=ResponseCode.SystemError)
    camera = db.session.query(Camera).first()
    if camera:
        rtsp=  camera.rtsp
        camera_ = cv2.VideoCapture(rtsp)
        success, frame = camera_.read()
        if success:
            # 将图像保存为临时文件
            temp_file = 'temp.jpg'
            cv2.imwrite(temp_file, frame)

            # 准备上传文件的请求数据
            files = {'file': open(temp_file, 'rb')}

            # 发送POST请求上传文件
            response = requests.post('http://127.0.0.1:6000/upload', files=files)

            # 检查上传结果
            if response.status_code == 200:
                res.update(code=ResponseCode.Success,data=response.content)
            else:
                res.update(code=ResponseCode.SystemError)

            # 删除临时文件
            # os.remove(temp_file)
    # if 'file' in request.files:
    #     file = request.files['file']
    #     data=dict(file=file)
    #     res.update(code=ResponseCode.Success,data=data)
    return res.data
@route(bp, '/getCamera', methods=["GET"])
def getCamera():
    res = ResMsg()
    res.update(code=ResponseCode.NoResourceFound)
    camera = db.session.query(Camera).first()
    if camera:
        data = dict(rtsp=camera.rtsp,interval=camera.interval)
        res.update(code=ResponseCode.Success,data=data)
    return res.data

@route(bp, '/setCamera', methods=["POST"])
def setCamera():
    res = ResMsg()
    try:
        res.update(code=ResponseCode.InvalidParameter)
        rtsp = request.json.get("rtsp")
        interval = request.json.get("interval")
        camera = db.session.query(Camera).first()
        if camera:
            camera.rtsp = rtsp
            camera.interval = interval
        else:
            camera = Camera(rtsp=rtsp, interval=interval)
            db.session.add(camera)
        db.session.commit()
        res.update(code=ResponseCode.Success)
    except Exception as e:
        res.update(code=ResponseCode.SystemError)
    return res.data
   

@route(bp,'/video_start', methods=["GET"])
def video_start():
    camera_ = db.session.query(Camera).first()
    if camera_:
        rtsp=  camera_.rtsp
        interval = camera_.interval
        return Response(gen_frames(rtsp,interval), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames(rtsp,frame_interval):
        camera = cv2.VideoCapture(rtsp)
        frame_count = 0
        while True:
            # start_time = time.time()
            success, frame = camera.read()
            if not success:
                break
            else:
                frame_count += 1
                if frame_count % frame_interval == 0:
                    frame_count = 0
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    
                    # end_time = time.time()
                    # duration = end_time - start_time
                    # print("函数运行时间：", duration, "秒")
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        camera.release()