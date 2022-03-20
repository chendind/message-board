# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.utils import mkresponse, ResponseMap
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 初始化orm
db = SQLAlchemy()

# 初始化flask-login
login_manager = LoginManager()
login_manager.session_protection = 'strong'

@login_manager.unauthorized_handler
def unauthorized():
    return mkresponse(code=ResponseMap.LOGIN_TIMEOUT)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    api_prefix = '/api'
    login_manager.init_app(app)

    # Create database if it does not exist.
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    try:
        if not database_exists(engine.url):
            create_database(engine.url, encoding='utf8mb4')
    except:
        pass

    db.init_app(app)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix=api_prefix + '/user')

    from .comment import comment as comment_blueprint
    app.register_blueprint(comment_blueprint, url_prefix=api_prefix + '/comment')

    return app
