from datetime import datetime

from sqlalchemy import Integer
from app.utils.core import db


class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    account = db.Column(db.String(20), nullable=True)  # 用户账号
    password = db.Column(db.String(20), nullable=True)  # 用户密码
    
class Camera(db.Model):
    """
    相机表
    """
    __tablename__ = 'camera'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rtsp = db.Column(db.String(20), nullable=True)  # rtsp地址
    interval = db.Column(Integer, nullable=True)  # 间隔时间
