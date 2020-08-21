'''SQL Alchemy objects'''
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app
from flaskapp import db, login_manager
#from flask_user import roles_required

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    address1 = db.Column(db.String(20), unique=False, nullable=False)
    address2 = db.Column(db.String(20), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    country = db.Column(db.String(20), unique=False, nullable=False)
    postcode = db.Column(db.String(20), unique=False, nullable=False)   
    phone = db.Column(db.String(20), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)
    cart = db.relationship('Cart', lazy=True)
    
    roles = db.relationship('Role', secondary='user_roles')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __init__(self, username, email, password, address1, address2, city, country, postcode, phone):
        self.username = username
        self.email = email
        self.password = password
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.country = country
        self.postcode = postcode
        self.phone = phone
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sterling = db.Column(db.DECIMAL, nullable=False)
    discounted_sterling = db.Column(db.DECIMAL, nullable=False)
    product_rating = db.Column(db.DECIMAL)
    quantity = db.Column(db.Integer, nullable=False)
    posts = db.relationship('Post', backref='product', lazy=True)
    productCategory = db.relationship('Category', secondary='product_category', lazy=True)
    productImages = db.relationship('ProductImages', backref='product', lazy=True)
    cart = db.relationship('Cart', lazy=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Product('{self.title}', '{self.date_posted}')"

class ProductImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    alt = db.Column(db.String(100), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id

    def __repr__(self):
        return f"Product('{self.category_id}', '{self.product_id}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    productCategory = db.relationship('Product', secondary='product_category', lazy=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Category('{self.id}', '{self.category_name}')"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_price = db.Column(db.DECIMAL, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_date}','{self.total_price}','{self.user_id}'')"

class OrderedProduct(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_id}','{self.product_id}','{self.quantity}')"

class SaleTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.DECIMAL, nullable=False)
    cc_number = db.Column(db.String(100), nullable=False)
    cc_type = db.Column(db.String(100), nullable=False)
    response = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_id}','{self.transactiondate}','{self.amount}', '{self.cc_number}','{self.cc_type}','{self.response}')"

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
