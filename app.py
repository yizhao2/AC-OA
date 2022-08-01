#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/3 下午5:39
# @Author  : xianzx
# @Email   : xianeamil@icloud.com
# @Site    :
# @File    : app.py
# @Software: PyCharm
import os
# 引入flask
from flask import Flask
from flask_restful import Api, request

from config import config
token_config = config.get_token_config()


# 创建WEB服务
app = Flask(__name__)
api = Api(app)


# 打开SYSTEM日志
from log import LoggerHandler
log_config = config.get_log_config()
loggerHandler = LoggerHandler(request, token_config)
app.logger.addHandler(loggerHandler)
app.logger.level = log_config['level']


# 引入OperationLogger和Auth
from log import OperationLogger
operationLogger = OperationLogger(token_config)
from auth import Auth
auth = Auth(token_config)
@app.before_request
def before_request():
    operationLogger.log(request)
    auth.auth(request)

@app.after_request
def after_request(response):
    operationLogger.log(request, response)
    return response


# 引入api并注册view
import views
from view import register_views
register_views(api, views)

if __name__ == '__main__':
    if os.getenv('RUNTIEM_ENV', 'debug') == 'debug':
        app.run(debug=True, port=5000, host='0.0.0.0')
    else:
        app.run(debug=False, port=5000, host='0.0.0.0')
    pass