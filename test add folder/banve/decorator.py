from functools import wraps
from flask import session, request, redirect, url_for
from flask_login import current_user


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/admin')

        return f(*args, **kwargs)

    return decorated_function


def check_user():
    if current_user.is_authenticated:
        return True
    else:
        return False