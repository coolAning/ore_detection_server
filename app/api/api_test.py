import logging

from flask import Blueprint

from app.models.model import User
from app.utils.core import db
from app.utils.response import ResMsg
from app.utils.util import route
from app.utils.code import ResponseCode
bp = Blueprint("test", __name__, url_prefix='/')

logger = logging.getLogger(__name__)


@route(bp, '/testdb', methods=["GET"])
def testdb():
    res = ResMsg()
    user = db.session.query(User).all()
    print(user)

    return res.data

@route(bp, '/test', methods=["GET"])
def test():
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    # 此处只需要填入响应状态码,即可获取到对应的响应消息
    res.update(code=ResponseCode.Success, data=test_dict)
    return res.data