import subprocess
from werkzeug.datastructures import FileStorage
import logging

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
        # 通过将一帧帧的图像返回，就达到了看视频的目的。multipart/x-mixed-replace是单次的http请求-响应模式，如果网络中断，会导致视频流异常终止，必须重新连接才能恢复
        return Response(gen_frames(rtsp,interval), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames(rtsp,frame_interval):
        camera = cv2.VideoCapture(rtsp)
        frame_count = 0
        while True:
            # start_time = time.time()
            # 一帧帧循环读取摄像头的数据
            success, frame = camera.read()
            if not success:
                break
            else:
                frame_count += 1
                if frame_count % frame_interval == 0:
                    frame_count = 0
                    # 将每一帧的数据进行编码压缩，存放在memory中
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    
                    # end_time = time.time()
                    # duration = end_time - start_time
                    # print("函数运行时间：", duration, "秒")
                    
                    # 使用yield语句，将帧数据作为响应体返回，content-type为image/jpeg
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')