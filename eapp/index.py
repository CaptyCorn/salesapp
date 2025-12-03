from flask import render_template, request, redirect
from flask_login import login_user, logout_user

from eapp import app, dao, login
from eapp.models import UserRole
import math

@app.route('/')
def index():
    return render_template('index.html',
                           pages = math.ceil(dao.count_products()/app.config['PAGE_SIZE']),
                           products=dao.get_product(kw=request.args.get('kw'),
                                                    category_id=request.args.get('category_id'),
                                                    page = request.args.get('page')))

@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    print(username, password)
    u = dao.auth_user(username=username, password=password)
    if u:
        print(u)
        login_user(user=u)

    next = request.args.get('next')
    return redirect(next if next else '/')

@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')

@app.context_processor
def common_response():
    return{
        'categories': dao.get_category()
    }

@login.user_loader
def load_user(pk):
    return dao.get_user_by_id(pk)

if __name__ == '__main__':
    from eapp import admin
    app.run(debug=True)
