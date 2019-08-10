# MyFlask

#### 学习过程

1. 第一章

   1. 虚拟环境的安装

   ```
   virtualenv venv
   source venv/bin/activate
   ```

   2. 代码运行

   ```
   export FLASK_APP=microblog.py 
   flask run
   # -- coding:utf-8 -- 放在开头，python下可写中文注释
   ```

2. 第二章
   在写templates时，其中的可替换部分用{{}}双括号，

   如{{title}}，在使用控制语句时用{% %}单括号，如``{% for post in posts %}{% endfor %}``

3. 第三章

   1. 在Python会话中验证SECRET_KEY时，``from microblog import App``，注意此时的App为从app中引进的类App
   2. ``flash('Login requested for  user {} , remember_me : {}' .format(form.username.data , form.remember_me.data)) ``flash用法中，显示表单中的数据时，{}用没有空格
   3. ``<meta charset="utf-8">``放在开头，html文件中可写中文注释
   4. url_for('index')后面加ivew function 的名称，而不是URL

4. 第四章

   1. pip install --upgrade dnspython 更新某个包

   2. 安装flask-sqlalchemy时，提示pyldap没安装，pyldap已经被python-ldap代替

   3. config.py中，设置数据库时，or  'sqlite:///' + os.path.join(basedir,'app.db') 在or的后面没有 /. 在model.py改动数据后，先生成一个新的迁移 ``flask db migrate -m "posts table" ``，然后将迁移应用到数据库``flask db upgrade.` 创建一个用户，并上传到数据库中。如果在会话执行的任何时候出现错误，调用db.session.rollback()会中止会话并删除存储在其中的所有更改。	


     ```
     u = User(username='john', email='john@example.com')
     db.session.add(u)
     db.session.commit()
     ```

   5. shell 中操作数据库用for 语句时，下面一行需要缩进

   6. flask shell的妙用

5. 第五章

6. 第六章

    1. Every time the database is modified it is necessary to generate a database migration. 

            flask db migrate -m "new fields in user model"
            flask db upgrade

    2. 数据库migrate时 -m 后面的内容不要输入中文

    3. 测试帐号 Guang Mujun wwzy123456

7. 第七章

      1. 设置调试模式，它是Flask在浏览器上直接运行一个友好调试器的模式。``export FLASK_DEBUG=1``
      2. 在调试模式下运行flask run，则可以在开发应用时，每当保存文件，应用都会重新启动以加载新的代码。

8. 第八章

     1. 数据库的变更

     ```
     flask db migrate -m "followers"
     flask db upgrade
     ```

     2. 运行测试组件

     		``(venv)$ python tests.py``

     3. ``AssertionError: View function mapping is overwriting an existing endpoint function: follow``

     		重复定义函数造成的错误

     4. 测试帐号 test1 test1@example.com 123  test2 test2@example.com 123
     5. 需要手动输入用户的个人主页URL，以此来进行关注或者取消关注

9. 第九章

  ``next_url = url_for('index', page=posts.next_num) \``	此处 \ 后面不能有空格，条件语句的另外一种用法``if posts.has_next else None.`` 主页与个人主页的分页原理相同，都是_post.html	

10. 第十章

       1. 在config.py中更改邮箱的相关配置
       2. 运行前，将邮箱的密码设置到环境变量中 ``export MAIL_PASSWORD='your-password'``
       3. 谷歌邮箱设置，信任不安全应用

11. 第十一章

            1. Bootstrap--CSS框架的一种
            2. 使用pip安装扩展时，命令行前面加上 sudo速度较慢，安装超时，用 ``pip --default-timeout=100 install``

            3. ``{% block body %}``全部替换成`` {%  block app_content %}``
            4. 渲染bootstrap表单时，加上``{% import 'bootstrap/wtf.html' as wtf %}``

12. 第十二章

         1. Moment.js是一个小型的JavaScript开源库，它将日期和时间转换成目前可以想象到的所有格式。
         2. ISO 8601标准格式如下：``{{ year }}-{{ month }}-{{ day }}T{{ hour }}:{{ minute }}:{{ second }}{{ timezone }}``。 我已经决定我只使用UTC时区，因此最后一部分总是将会是Z，它表示ISO 8601标准中的UTC。

**部署篇：**

1. 需求文件

   `pip freeze >requirements.txt`(2018.8.3生成的需求文件为适应服务器的文件)

2. Putty和WinScp的使用
   1. Putty中输入IP地址，打开后，输入服务器的帐号和密码即可
   2. WinScp是使用本地的SSHm密钥登陆
   3. Putty中输入git clone https://gitee.com/guangmujun/DHSDK.git后输入帐号密码，将项目克隆到服务器上
3. 安装虚拟环境

````
virtualenv venv （在microblog文件目录下创建）
source venv/bin/activate
````

4. 安装需求文件

   ``pip install -r requirements.txt`

5. 安装gunicorn

   pip安装速度慢？ 用国内镜像，如安装gunicorn

   `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn`

6. 运行应用（调试）

   1. 先输入环境变量``export FLASK_APP=microblog.py```
   2. ```gunicorn -b 0.0.0.0:8000 -w 4 microblog:App`
   3. 此时，浏览器输入：http://服务器地址：8000可访问应用
   4. -b 选项告诉gunicorn在哪里监听请求，在8000端口上监听了内部网络接口
   5. -w 选项配置gunicorn将运行多少worker， 拥有四个进程可以让应用程序同时处理多达四个客户端
   6. microblog:App参数告诉gunicorn如何加载应用程序实例。

7. 配置nginx

   在 /etc/nginx/nginx.conf

   ```
   server{
   		listen		80;				监听端口号
   		server_name	guangmujun.cn;			解析域名
   		location / {
   			root	 /usr/share/nginx/html;
   			index	index.html index.htm;
   			proxy_pass http://guangmujun.cn:8000;	重定向
   		}
   ```

   ps:配置文件修改后，[root@server ~]# service nginx start 服务重启后才能生效

   浏览器访问guangmujun.cn 即可访问应用

8. 邮箱 使用前需设置邮箱密码相关的环境变量

