'''Initialisation class'''
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskapp.config import Config
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
ma = Marshmallow()
csrf = CSRFProtect()


def create_app(config_class=Config):
    '''Create the app and register blueprints'''
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ma.init_app(app)
    csrf.init_app(app)
    
    from flaskapp.users.routes import users
    from flaskapp.posts.routes import posts
    from flaskapp.admin.routes import admin
    from flaskapp.products.routes import products
    from flaskapp.main.routes import main
    from flaskapp.errors.handlers import errors
    from flaskapp.api.api import apibp
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(admin)
    app.register_blueprint(products)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(apibp)

    return app
    
