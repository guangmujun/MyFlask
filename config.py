# -*- coding:utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'						#??????
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')  or  'sqlite:///' + os.path.join(basedir,'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = 'smtp.sina.com'
   	MAIL_PORT = 25
    	MAIL_USE_TLS = True
    	MAIL_USERNAME = 'wangyuahng18@sina.com'
    	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    	ADMINS = ['wangyuahng18@sina.com']
	POSTS_PER_PAGE = 6		#每一页显示的数据长度
