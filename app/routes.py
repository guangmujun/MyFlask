# -*- coding:utf-8 -*-
from app import App , db
from flask import render_template , flash , redirect , url_for , request
from app.forms import LoginForm , RegistrationForm , EditProfileForm , PostForm ,ResetPasswordRequestForm , ResetPasswordForm
from app.models import User , Post
from flask_login import current_user , login_user , logout_user , login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email

@App.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@App.route('/', methods = ['GET' , 'POST'])
@App.route('/index', methods = ['GET' , 'POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body = form.post.data , author = current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live! --Guang Mujun')
		return redirect(url_for('index'))					#重定向来响应Web表单提交产生的POST请求
	page = request.args.get('page' , 1 , type = int)				#request.args访问查询字符串中的参数 http://localhost:5000/index?page=2
	posts = current_user.followed_posts().paginate(
		page , App.config['POSTS_PER_PAGE'] , False )			#从数据库中获取用户感兴趣的用户动态。paginate()方法支持分页，三个参数：1.开始的页码2.每页的数据量3.错误布尔标记。
	next_url = url_for('index', page=posts.next_num) \
        		if posts.has_next else None					#has_next: 当前页之后存在后续页面时为真 next_num: 下一页的页码
  	prev_url = url_for('index', page=posts.prev_num) \
        		if posts.has_prev else None					#has_prev: 当前页之前存在前置页面时为真 prev_num: 上一页的页码
	return render_template('index.html', title='Home', form=form,
                          					posts=posts.items, next_url=next_url,
                          					prev_url=prev_url)#paginate()的返回是Pagination类的实例，items属性返回数据内容列表

@App.route('/explore')
@login_required
def explore():
	page = request.args.get('page' , 1 , type = int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(
		page , App.config['POSTS_PER_PAGE'] , False )
	next_url = url_for('explore', page=posts.next_num) \
        		if posts.has_next else None
  	prev_url = url_for('explore', page=posts.prev_num) \
        		if posts.has_prev else None
	return render_template('index.html', title='Home', posts=posts.items,
	 						next_url=next_url, prev_url=prev_url)

@App.route('/login' , methods = ['GET' , 'POST'])
def login():
	if current_user.is_authenticated:																			#验证是否用户已经登陆
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():																				#浏览器发送POST请求时，form.validate_on_submit()会验证表单数据，通过验证后返回True
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password! --Guang Mujun')
			return redirect(url_for('login'))
		login_user(user , remember = form.remember_me.data)
		next_page =request.args.get('next')
		if not next_page or url_parse(next_page).netloc != ' ':
			next_page =url_for('index')
		return redirect(next_page)
	return render_template('login.html' , title = 'Sign In' , form =form )

@App.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@App.route('/register', methods = ['GET' , 'POST'])
def register():
	if current_user.is_authenticated:																			
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username = form.username.data , email = form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash ('Have fun , you have been a registered user ! --Guang Mujun')
		return redirect (url_for ('login'))
	return render_template('register.html' , title = 'Regitser' , form =form)

@App.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username = username).first_or_404()
	page = request.args.get('page' , 1 ,type = int)
	posts =user.posts.order_by(Post.timestamp.desc()).paginate(
		page , App.config['POSTS_PER_PAGE'] , False)
	next_url = url_for('user' , username = user.username , page = posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('user' , username = user.username , page = posts.prev_num) \
		if posts.has_prev else None
	return render_template('user.html' , title = 'User' ,  user = user , posts = posts.items ,
							next_url = next_url , prev_url = prev_url )

@App.route('/edit_profile', methods = ['GET' , 'POST'])
@login_required
def edit_profile():
		form = EditProfileForm(current_user.username)#要用到目前的用户名，来检验修改后的用户名是否可用
		if form.validate_on_submit():
			current_user.username = form.username.data
			current_user.about_me = form.about_me.data
			db.session.commit()
			flash('Your changes have been saved. --Guang Mujun')
			return redirect(url_for('edit_profile'))
		elif request.method == 'GET':
			form.username.data = current_user.username
			form.about_me.data = current_user.about_me
		return render_template('edit_profile.html' , title = 'Edit Profile' ,form = form )

@App.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username = username).first()
	if user is None:
		flash ('User {} not found !' .format(username))
		return redirect(url_for('index'))
	if user == current_user:
		flash('You can not follow yourself! --Guang Mujun')
		return redirect(url_for('user' , username = username))
	current_user.follow(user)
	db.session.commit()
	flash('You are following {} ! --Guang Mujun' .format(username))
	return redirect(url_for('user' , username = username))

@App.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username = username).first()
	if user is None:
		flash ('User {} not found !' .format(username))
		return redirect(url_for('index'))
	if user == current_user:
		flash('You can not unfollow yourself! --Guang Mujun')
		return redirect(url_for('user' , username = username))
	current_user.unfollow(user)
	db.session.commit()
	flash('You are not following {}! --Guang Mujun' .format(username))
	return redirect(url_for('user' , username = username))

@App.route('/reset_password_request', methods = ['GET' , 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('Check your email for the instructions to reset your password --Guang Mujun')
		return redirect(url_for('login'))
	return render_template('reset_password_request.html' , title = 'Reset Password' , form = form )

@App.route('/reset_password/<token>', methods = ['GET' , 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user =User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset. --Guang Mujun')
		return redirect(url_for('login'))
	return render_template('reset_password.html' , form = form)
