# -*- coding: utf-8 -*-
from . import user
from flask_login import login_user, logout_user, login_required, current_user
from flask import request, session
from app.utils import mkresponse, ResponseMap
from app.models import User
from app.user.service import isDuplicateUser, addUser, getUserByUsernameOrEmail

# Sign up
# 用户注册
@user.route('/signUp', methods = ['POST'])
def signUp():
    username = request.form.get('username', type = str, default = None)
    email = request.form.get('email', type = str, default = None)
    password = request.form.get('password', type = str, default = None)
    # Check necessary parameters
    # 检查必要的参数
    if username is None or email is None or password is None:
        return mkresponse(code = ResponseMap.REQUEST_PARAMS_ERROR)
    # Check if the username format is correct
    # 检查用户名格式是否正确
    if not User.checkUsername(username):
        return mkresponse(code = ResponseMap.USERNAME_FORMAT_ERROR)
    # Check if the email format is correct
    # 检查邮箱格式是否正确
    if not User.checkEmail(email):
        return mkresponse(code = ResponseMap.EMAIL_FORMAT_ERROR)
    # Check if the password format is correct
    # 检查密码格式是否正确
    if not User.checkPassword(password):
        return mkresponse(code = ResponseMap.PASSWORD_FORMAT_ERROR)
    # Check if there is the same username/email as an existing user
    # 检查是否与已有的用户重名
    if isDuplicateUser(username, email):
        return mkresponse(code = ResponseMap.USER_EXIST)
    addUser(username, email, password)
    return mkresponse(code=ResponseMap.ADD_SUCCESS)

# Sign in
# 用户登录
@user.route('/signIn', methods = ['POST'])
def signIn():
    username = request.form.get('username', type = str, default = None)
    email = request.form.get('email', type = str, default = None)
    password = request.form.get('password', type = str, default = None)
    remember = request.form.get('remember', type = int, default = 0)
    remember = bool(remember)
    # Check necessary parameters
    # 检查必要的参数
    if username is None and email is None:
        return mkresponse(code = ResponseMap.REQUEST_PARAMS_ERROR)
    # Get users by username or email
    # 根据用户名或邮箱获得用户
    user = getUserByUsernameOrEmail(username, email)
    if user is None:
        return mkresponse(code = ResponseMap.USER_NON_EXIST, message = '您尚未注册，请先注册再登录')
    # Verify user password
    # 校验用户密码
    if user.verifyPassword(password):
        login_user(user, remember = remember)
        # `permanent` is set to `false`` to make the session invalid after closing the browser
        # `permanent`设置为`false`使得关闭浏览器后session失效；
        session.permanent = remember
        return mkresponse()
    else:
        return mkresponse(code = ResponseMap.PASSWORD_ERROR)

# Sign out
# 用户登出
@user.route('/signOut', methods = ['POST'])
@login_required
def signOut():
    logout_user()
    return mkresponse()

# User gets his own data
# 用户获得自己的数据
@user.route('/self', methods = ['get'])
@login_required
def self():
    return mkresponse(data = current_user.toDict())
