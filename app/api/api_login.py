import logging

from flask import Blueprint

from app.models.model import User
from app.utils.core import db
from flask import request
from app.utils.response import ResMsg
from app.utils.util import route
from app.utils.code import ResponseCode

bp = Blueprint("user", __name__, url_prefix='/user')

logger = logging.getLogger(__name__)

@route(bp, '/login', methods=["POST"])
def login():
    res = ResMsg()
    res.update(code=ResponseCode.AccountOrPassWordErr)
    user = db.session.query(User).filter(User.account == request.json.get("account")).first()
    if user:
        if user.password == request.json.get("password"):
            res.update(code=ResponseCode.Success)
    return res.data