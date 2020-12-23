from flask_admin import BaseView, expose
from banve import db, admin
from flask_login import current_user, logout_user
from banve.models import *
from flask import  redirect
from flask_admin.contrib.sqla import ModelView

class ModelView(ModelView):
    column_display_pk = True
    can_create = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


class logoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(ManagerUser,db.session))
admin.add_view(ModelView(NormalUser,db.session))
admin.add_view(ModelView(Airport,db.session))
admin.add_view(ModelView(Plane,db.session))
admin.add_view(ModelView(Route,db.session))
admin.add_view(ModelView(Flight,db.session))
admin.add_view(ModelView(PriceTable,db.session))
admin.add_view(logoutView(name="Logout"))
