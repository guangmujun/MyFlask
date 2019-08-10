# -*- coding:utf-8 -*-
from datetime import datetime
from app import db , login ,App
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time 
import jwt


@login.user_loader
def load_user(id):
	return User.query.get(int(id))

#没有声明为模型，是因为这只是一个由外键构成的辅助表
followers = db.Table('followers' ,
	db.Column('followed_id' , db.Integer , db.ForeignKey('user.id')),
	db.Column('follower_id' , db.Integer , db.ForeignKey('user.id'))
	 )

class User(UserMixin,db.Model):
	id = db.Column(db.Integer , primary_key = True)
	username = db.Column(db.String(64) , index = True ,unique = True )
	email = db.Column(db.String(120) , index = True ,unique = True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post' , backref = 'author' , lazy = 'dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime , default = datetime.utcnow)
	followed = db.relationship(
		'User' , secondary = followers ,#secondary 指定用于该关系的关联表
		primaryjoin = (followers.c.follower_id == id),#primaryjoin 通过关联表关联到关注者的条件 followers.c.follower_id 引用followers表中的follower_id列
		secondaryjoin = (followers.c.followed_id == id),#secondaryjoin 通过关联表关联到被关注者的条件 
		backref = db.backref('followers' , lazy = 'dynamic') , lazy = 'dynamic'	)

	def __repr__(self):
		return '<User {}>' .format(self.username)

	def set_password(self,password):
		self.password_hash = generate_password_hash(password)

	def check_password (self, password):
		return check_password_hash(self.password_hash,password)

	def avatar(self , size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}' .format(digest , size)

	def myphoto(self,size):
		return 'https://www.gravatar.com/avatar/25b55357c054e4b934879d9598d07232?s={}'.format(size)

	def follow(self , user):
		if not self.is_following(user):
			self.followed.append(user)#关注

	def unfollow(self , user):
		if self.is_following(user):
			self.followed.remove(user)#取消关注

	def is_following(self , user):
		return self.followed.filter(
			followers.c.followed_id == user.id).count () >0 #确定是否已经关注 count（）返回结果的数量

	def followed_posts(self):
		followed =  Post.query.join(
			followers , (followers.c.followed_id == Post.user_id)	).filter(
				followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id = self.id)
		return followed.union(own)	.order_by(Post.timestamp.desc())

	def get_reset_password_token(self, expires_in=6000):
		return jwt.encode(
			{'reset_password':self.id , 'exp':time() + expires_in},
			App.config['SECRET_KEY'] , algorithm = 'HS256').decode('utf-8')
	@staticmethod
	def verify_reset_password_token(token):
		try:
			id =jwt.decode(token , App.config['SECRET_KEY'],
				algorithm = ['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

class Post(db.Model):
	id = db.Column(db.Integer , primary_key = True )
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime , index = True , default = datetime.utcnow)
	user_id = db.Column(db.Integer , db.ForeignKey ('user.id'))					   
#user是数据库表的名称，Flask-SQLAlchemy自动设置类名为小写来作为对应表的名称

	def __repr__(self):
		return '<Post {}>' .format(self.body)


	
