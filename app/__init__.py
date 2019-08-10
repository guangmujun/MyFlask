# -*- coding:utf-8 -*-
from  flask import  Flask 					#falsk & app are package , Flask & App are  instance
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail

import logging					#通过logging包写错误日志
from logging.handlers import SMTPHandler 
from logging.handlers import RotatingFileHandler
import os

App = Flask (__name__)
App.config.from_object(Config)			#????
db = SQLAlchemy(App)
migrate = Migrate(App , db)
login = LoginManager(App)
login.login_view = 'login'
bootstrap = Bootstrap(App)
moment = Moment(App)
mail = Mail(App)

if not App.debug:				#为Flask的日志对象app.logger添加一个SMTPHandler的实例
	if not os.path.exists('logs'):#根目录下创建logs文件夹
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/microblog.log' , maxBytes=10240 , backupCount=10)#日志文件大小限制为10kb，保留最后10个日志文件作为备份
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s :%(message)s [in %(pathname)s :%(lineno)d ] '))#时间戳、日志记录级别、消息、日志来源的源代码文件、行号
	file_handler.setLevel(logging.INFO)#INFO为日志记录级别
	App.logger.addHandler(file_handler)

	App.logger.setLevel(logging.INFO)
	App.logger.info('Microblog startup ---- Guang Mujun')


from app import routes , models	,errors				
#because routes.py use "from app import App" 这里和routes.py中必须有，相呼应
	
