from functools import wraps
from flask import flash, abort
from flask_login import current_user
from flaskapp.models import Role, UserRoles

def roles_required(access_level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            r = Role.query.filter(Role.name == access_level).first()
            if r:
                user_role = UserRoles.query.filter(UserRoles.user_id == current_user.id).filter(UserRoles.role_id == r.id).first()
                if user_role:
                    print(user_role)
                    return func(*args, **kwargs)
                else:
                    flash("You do not have permission to view that page", "warning")
                    abort(403)
            else:
                flash("Role Not Found!", "warning")
                abort(403)
        return wrapper
    return decorator