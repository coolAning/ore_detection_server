import base64
from werkzeug.datastructures import FileStorage
import logging

from flask import Blueprint

from app.models.model import User
from app.utils.core import db
from flask import request
from app.utils.response import ResMsg
from app.utils.util import route
from app.utils.code import ResponseCode

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