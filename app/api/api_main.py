import base64
from werkzeug.datastructures import FileStorage
import logging

from flask import Blueprint,Response

from app.models.model import User
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


@route(bp,'/video_start', methods=["GET"])
def video_start():
    # 通过将一帧帧的图像返回，就达到了看视频的目的。multipart/x-mixed-replace是单次的http请求-响应模式，如果网络中断，会导致视频流异常终止，必须重新连接才能恢复
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

 
def gen_frames():
    camera = cv2.VideoCapture('rtsp://admin:djn123456@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0&proto=Private3')
    while True:
        # start_time = time.time()
        # 一帧帧循环读取摄像头的数据
        success, frame = camera.read()
        if not success:
            break
        else:
            # 将每一帧的数据进行编码压缩，存放在memory中
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # end_time = time.time()
            # duration = end_time - start_time
            # print("函数运行时间：", duration, "秒")
            
            # 使用yield语句，将帧数据作为响应体返回，content-type为image/jpeg
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')