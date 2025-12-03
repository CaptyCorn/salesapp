from eapp.models import Category, Product, User, UserRole
import hashlib
from eapp import app

def get_category():
    return Category.query.all()

def get_product(kw=None, category_id=None, page=1):
    products = Product.query

    if category_id:
        products = products.filter(Product.category_id==category_id)

    if kw:
        products = products.filter(Product.name.contains(kw))

    if page:
        page = int(page)
        page_size = app.config.get('PAGE_SIZE', 6)
        start = (page - 1) * page_size
        products = products.slice(start, start + page_size)

    return products.all()

def count_products():
    return Product.query.count()

def get_user_by_id(id):
    return User.query.get(id)

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username == username.strip(),
                          User.password == password).first()