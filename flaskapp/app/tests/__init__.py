# -*- coding: utf-8 -*-
from config import Config
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:aa111111@mb_mysql/test_message_board?charset=utf8mb4'