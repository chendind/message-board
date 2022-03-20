# -*- coding: utf-8 -*-
import datetime

class Config:
    NAME_EN = 'MESSAGE-BOARD'
    NAME_ZH = '留言板'
    SECRET_KEY = 'cb9c2cfcf9b6b17f4aee0ec3623a1940'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=1)
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=31)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DefaultConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:U72lDfv6@mb_mysql/message_board?charset=utf8mb4'

config = {
    'default': DefaultConfig
}
