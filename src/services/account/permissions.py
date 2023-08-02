from functools import wraps

from flask import abort, flash
from flask_login import current_user


def user_active_account(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_active:
            abort(403)
        return func(*args, **kwargs)
    return decorated_function
