#-*- coding: utf-8 -*-
import time, datetime, json

# Convert datetime to timestamp
# 将datetime格式转换为时间戳
def getTimestamp(dt):
    try:
        if type(dt) == datetime.timedelta:
            return dt.seconds
        else:
            return time.mktime(dt.timetuple())
    except:
        return None

# Convert timestamp to formatted string
# 格式化时间戳
def getFormatTime(timestamp, format = '%Y-%m-%d %H:%M:%S'):
    try:
        return time.strftime(format, time.localtime(timestamp))
    except:
        return None

# API response code, HTTP status code and description
# 定义了接口返回码、HTTP状态码、描述
class ResponseMap():
    SUCCESS = 0, 200, '成功'
    ADD_SUCCESS = 0, 201, '成功'
    REQUEST_PARAMS_ERROR = 1, 400, '参数错误'
    LOGIN_TIMEOUT = 2, 401, '登录超时'
    PASSWORD_ERROR = 3, 401, '密码错误'
    USER_EXIST = 4, 403, '用户已注册'
    USERNAME_FORMAT_ERROR = 5, 403, '用户名格式错误（只能使用字母和数字，长度在5~20之间）'
    EMAIL_FORMAT_ERROR = 6, 403, '邮箱格式错误'
    PASSWORD_FORMAT_ERROR = 7, 403, '密码格式错误（长度在8~20之间，至少包含一个大写、一个小写、一个数字、一个特殊符号）'
    MESSAGE_CONTENT_FORMAT_ERROR = 8, 403, '留言格式错误（留言长度在3~200字之间）'
    USER_NON_EXIST = 9, 403, '用户不存在'

# API response constructor
# 接口相应数据函数
def mkresponse(code = ResponseMap.SUCCESS, message = None, data = {}):
    return json.dumps({
        'code': code[0],
        'message': message if message is not None else code[2],
        'data': data
    }), code[1]

