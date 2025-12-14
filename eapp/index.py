from flask import render_template, request, redirect, jsonify, session
from flask_login import login_user, logout_user

from eapp import app, dao, login, utils
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

@app.route('/cart')
def cart_view():
    return render_template('cart.html')

@app.route('/register', methods=['post'])
def register_process():
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    if password != confirm:
        err_msg = 'Mật khẩu không trùng khớp.'
        return render_template('/register.html', err_msg=err_msg)

    try:
        avatar = request.files.get('avatar')
        u = dao.add_user(avatar=avatar,
                         name=request.form.get('name'),
                         username=request.form.get('name'),
                         password=password)
    except Exception as ex:
        return render_template('/register.html', err_msg='Hệ thống đang có lỗi')

    return redirect('/login')


@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    next = request.args.get('next')
    return redirect(next if next else '/')

@app.route('/api/carts', methods=['post'])
def add_to_cart():
    data = request.json
    cart = session.get('cart')

    if not cart:
        cart = {}

    id, name, price = str(data.get('id')), data.get('name'), data.get('price')

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    """
           {
               "1": {
                   "id": 1,
                   "name": "...",
                   "price": 99,
                   "quantity": 2
               }, "2": {
                   "id": 2,
                   "name": "...",
                   "price": 99,
                   "quantity":5
               }
           }
       """

    session['cart'] = cart
    print(cart)
    return jsonify(utils.count_cart(cart))

@app.route('/api/carts/<id>', methods=['put'])
def update_to_cart(id):
    cart = session.get('cart')
    if cart and id in cart:
        quantity = int(request.json.get('quantity'))
        cart[id]['quantity'] = quantity

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))

@app.route('/api/carts/<id>', methods=['delete'])
def delete_to_cart(id):
    cart = session.get('cart')
    if cart and id in cart:
        del cart[id]

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))

@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')

@app.context_processor
def common_response():
    return{
        'categories': dao.get_category(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }

@login.user_loader
def load_user(pk):
    return dao.get_user_by_id(pk)

if __name__ == '__main__':
    from eapp import admin
    app.run(debug=True)
