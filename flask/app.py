from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user
from flask_login import UserMixin

import os
import sys
import click

# create a Flask object
app = Flask(__name__, static_url_path='/static')


# ---------------------------------------------Flask基础路由、传参等功能展示------------------------------


# 主页，快捷切换不同展示页面
@app.route('/home')
def home():
    return render_template('home_page.html')


# create URL via route()
# the request of '/' turns into the call of hello()
# the function hello() returns a string text and rendered in the browser
@app.route('/')
def hello():
    return 'hello world'


# the function embedded_html returns a full html code
# which is the original way to insert html
@app.route('/embedded-html')
def embedded_html():
    user = {'username': 'Andy', 'age': '22'}
    return f'''
    <html>
        <head>
            <title>Templating</title>
        </head>
        <body>
            <h1>Hello, ''' + user['username'] + '''! you’re ''' + user['age'] + ''' years old.</h1>
            <br>
            <form action="/home">
                <button type="submit">Home</button>
            </form>
        </body>
    </html>
    '''


# insert a html form with submit to trigger a default GET request
# parameter can be passed by the url
@app.route('/pass-parameter')
def pass_parameter():
    key = request.values.get('key')
    return f'''
    <form action='/redirect'>
        Username: <input name='username' value='{key}'>
        <br>
        Password: <input name='pwd'>
        <br>
        <input type='submit'>
    </form>
    <br>
    <form action="/home">
        <button type="submit">Home</button>
    </form>
    '''


@app.route('/redirect')
def show():
    name = request.values.get('username')
    pwd = request.values.get('pwd')
    return f'''
    <p>Username={name}, Password={pwd}</p>
    <br>
    <form action="/home">
        <button type="submit">Home</button>
    </form>
    '''


# use independent html template to render web page
# by calling render_template()
# parameter can be passed via URL
@app.route('/temp')
@app.route('/temp/<name>')
def temp(name=None):
    return render_template('index.html', name=name)


# 用户输入的数据会包含恶意代码，所以不能直接作为响应返回
# 需要使用escape()函数对username变量进行转义处理
# 比如把 < 转换成 &lt;
# 这样在返回响应时浏览器就不会把它们当做代码执行
@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile is shown here'.format(escape(username))


# url_for() for url building
# with app.test_request_context():
#    print(url_for('profile', username='url-test'))


# http methods
@app.route('/form', methods=['GET', 'POST'])
def http_method():
    if request.method == 'POST':
        return show_the_form()
    else:
        return render_template('form.html')


# Use request.form to access the data transmitted in a POST/PUT request
def show_the_form():
    username = request.form['username']
    email = request.form['email']
    hobbies = request.form['hobbies']
    return redirect(url_for('show_form',
                            username=username,
                            email=email,
                            hobbies=hobbies))


# Use request.args.get to access the parameters submitted in the URL(?key=value)
@app.route('/show_form', methods=['GET'])
def show_form():
    username = request.args.get('username')
    email = request.args.get('email')
    hobbies = request.args.get('hobbies')
    return render_template('show_form.html',
                           username=username,
                           email=email,
                           hobbies=hobbies)


# Use static folder to serve CSS and JS code
@app.route('/full')
def show_full_page():
    return render_template('full.html')


# ----------------------------------------------数据库引入---------------------------------------
# 如果是 Windows 系统，使用三个斜线
# 否则使用四个斜线
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


# 写入一个 SQLALCHEMY_DATABASE_URI 变量
# 来告诉 SQLAlchemy 数据库连接地址
# we use SQLite for example here
# 关闭对模型修改的监控: SQLALCHEMY_TRACK_MODIFICATIONS set to false
# 在扩展类实例化前加载配置
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 在扩展类实例化前加载配置
# 初始化数据库扩展，传入程序实例 app
db = SQLAlchemy(app)


# 创建数据库模型
class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


# 自定义一个自动执行创建数据库表的命令

# 注册为命令
@app.cli.command()
# 设置选项
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database"""
    # 判断是否输入了选项
    if drop:
        db.drop_all()
    db.create_all()
    # 输出提示信息
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Kaijie'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


# 创建admin user
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')


# --------------------------------------------数据 & 页面渲染 & CRUD操作------------------------------------


# 在主页视图读取数据库记录
@app.route('/data')
def show_database():
    users = User.query.all()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('database.html', users=users, movies=movies)


# 自定义404错误页面模板
# 使用 app.errorhandler() 装饰器注册一个错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 注册一个模板上下文处理函数来统一注入每一个模板的上下文环境中
@app.context_processor
def inject_user():
    user = current_user
    return dict(user=user)


@app.context_processor
def inject_movies():
    movies = Movie.query.all()
    return dict(movies=movies)


# 基于base.html基模板的继承页面
@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    if request.method == 'POST':
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('watchlist'))  # 重定向到主页
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('watchlist'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('New item created.')
        return redirect(url_for('watchlist'))

    return render_template('watch-list.html')


app.config['SECRET_KEY'] = 'dev'


@app.route('/watchlist/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('watchlist'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/watchlist/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required  # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('watchlist'))  # 重定向回主页


# 设置页面，支持修改用户的名字
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('watchlist'))

    return render_template('settings.html')


# ---------------------------------------------接入用户认证----------------------------------------


login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


# 用户login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('watchlist'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


# 用户signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username exists. Try again.')
            return redirect(url_for('signup'))

        new_user = User(name=name, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('New user created.')
        return redirect(url_for('login'))

    return render_template('signup.html')


# 用户logout
@app.route('/logout')
@login_required  # 用于视图保护
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('watchlist'))  # 重定向回首页


# ---------------------------------------------程序执行入口----------------------------------------


if __name__ == '__main__':
    app.run(debug=True, port="8080")
