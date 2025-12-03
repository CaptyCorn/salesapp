from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user

from eapp import app, db
from eapp.models import Category, Product, UserRole

from flask_admin import Admin, expose, BaseView

admin = Admin(app=app, name='eSaleApp')

class AuthenticatedModelView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ProductView(AuthenticatedModelView):
    can_export = True
    column_list = ['id', 'name', 'price', 'category_id']
    column_filters = ['id', 'name', 'price']
    column_editable_list = ['name']
    edit_modal = True

class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self) -> bool:
        return current_user.is_authenticated

admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))