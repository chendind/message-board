# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy import func, text
import re
from flask_login import UserMixin
from app.utils import getTimestamp, getFormatTime
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class baseModel(db.Model):
    __abstract__ = True
    noShowList = []
    def toDict(self, noShowList=[]):
        noShowList += self.noShowList or []
        dict = {}
        for col in self.__table__.columns:
            if col.name not in noShowList:
                if isinstance(col.type, db.DateTime):
                    value = getTimestamp(getattr(self, col.name))
                    dict[col.name + '_str'] = getFormatTime(value)
                else:
                    value = getattr(self, col.name)
                dict[col.name] = value
        return dict


class User(UserMixin, baseModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(64), unique=True)
    # 密码hash值
    password_hash = db.Column(db.String(128))
    create_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    noShowList = ['password_hash']

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码是否正确
    def verifyPassword(self, password):
        return check_password_hash(self.password_hash, password)

    # 检查用户名格式
    @staticmethod
    def checkUsername(username):
        # username需要检查：不可为空，只能使用字母和数字，长度在5~20之间，不能与已有用户名重复
        pattern = re.compile('^[a-zA-Z\d]{5,20}$')
        return re.match(pattern, username) is not None

    # 检查邮箱格式
    @staticmethod
    def checkEmail(email):
        # email需要检查：不可为空，格式要正确，不能与已有email重复。为简单起见，不需要发送邮件确认
        # email长度不可超过数据库字段限制
        pattern = re.compile('^[a-zA-Z\d_-]+@[a-zA-Z\d_-]+(\.[a-zA-Z]+)+$')
        return re.match(pattern, email) is not None and len(email) <= 64

    # 检查密码格式
    @staticmethod
    def checkPassword(password):
        # password需要检查：不可为空，长度在8~20之间，至少包含一个大写、一个小写、一个数字、一个特殊符号
        pattern = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[-@_!#$%^&*()<>?/\|}{~:\.\'\"+=】【\]\[;：；‘、｜，。》《？」「～·])[-@_!#$%^&*()<>?/\|}{~:\.\'\"+=】【\]\[;：；‘、｜，。》《？」「～·A-Za-z\d]{8,20}$')
        return re.match(pattern, password) is not None

class Comment(baseModel):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    # 内容
    content = db.Column(db.String(256))
    # 始祖留言id，如果是第一级留言，则为None
    ancestor_comment_id = db.Column(db.Integer, default=None)
    # 父留言id，如果是第一级留言，则为None
    parent_comment_id = db.Column(db.Integer, default=None)
    create_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    update_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    # 检查邮箱格式
    @staticmethod
    def checkContent(content):
        # 留言长度在3~200字之间，可以为中文
        return type(content) == str and len(unicode(content, 'utf-8')) >= 3 and len(unicode(content, 'utf-8')) <= 200