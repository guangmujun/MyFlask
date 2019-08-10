# -*- coding:utf-8 -*-
from app import App ,db
from app.models import User , Post

@App.shell_context_processor						# 当flask shell命令运行时，它会调用这个函数并在shell会话中注册它返回的项目。
def make_shell_context():
	return {'db': db , 'User': User ,'Post': Post}			#return {}
