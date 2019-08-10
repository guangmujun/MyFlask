# -*- coding:utf-8 -*-
from flask import render_template
from app import App , db

@App.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404	#renturn后面的404和500是错误代码编码，这是错误界面，希望响应的状态码能反映出来
										#正常情况下，是默认返回200，即成功响应的代码，所以默认时不用写
@App.errorhandler(500)
def internal_error(error):
	db.session.rollback()				#为了保证任何失败数据库会话不对数据库造成干扰，使用数据库回滚
	return render_template('500.html'), 500
