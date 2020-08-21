from flaskapp.models import Product, Post, ProductImages, Order, Cart, ProductCategory, Category, User, SaleTransaction, OrderedProduct, Role, UserRoles
from flask_login import current_user
from flask import abort, current_app
from flaskapp import db, bcrypt
from flaskapp.users.utils import save_picture
from sqlalchemy.sql import func
import os

def get_product(product_id):
    return Product.query.get_or_404(product_id)

def has_products():
    return Product.query.count() > 0

def get_product_posts(product):
    return Post.query.filter_by(product=product).order_by(Post.date_posted.desc())

def get_product_images(product_id):
    return ProductImages.query.filter_by(product_id=product_id).order_by(ProductImages.uploaded_at.desc())

def get_products_with_image():
    return Product.query.join(ProductImages).filter(Product.id == ProductImages.product_id).order_by(Product.date_posted.desc())\
        .add_columns(Product.id, Product.title, Product.discounted_sterling, Product.product_rating, Product.quantity)\
        .add_columns(ProductImages.image_file, ProductImages.alt).group_by(Product.id)

def get_products_with_image_of_cat(category_id):
    return Product.query.join(ProductCategory).filter(Product.id == ProductCategory.product_id)\
        .filter(ProductCategory.category_id == category_id).join(ProductImages).filter(Product.id == ProductImages.product_id).order_by(Product.date_posted.desc())\
        .add_columns(Product.id, Product.title, Product.discounted_sterling, Product.product_rating, Product.quantity)\
        .add_columns(ProductImages.image_file, ProductImages.alt).group_by(Product.id)

def get_orders():
    return Order.query.filter(Order.user_id == current_user.id)

def get_cart_items():
    return Cart.query.filter(Cart.user_id==current_user.id)

def get_cart_item(product_id):
    return Cart.query.filter(Cart.user_id==current_user.id, Cart.product_id==product_id).first()

def get_comment(post_id):
    return Post.query.get_or_404(post_id)

def delete_comment(post_id):
    post = get_comment(post_id)
    if post.author != current_user:
        abort(403)

    product = get_product(post.product_id)
    db.session.delete(post)
    db.session.commit()
    update_product_rating(product)

def update_comment(post, title, content, rating):
    post.title = title
    post.content = content
    post.rating = rating
    db.session.commit()
    product = get_product(post.product_id)
    update_product_rating(product)

def create_comment(title, content, rating, author, product):
    post = Post(title=title, content=content, rating=rating, author=author, product=product)

    db.session.add(post)
    db.session.commit()
    update_product_rating(product)

def update_product_rating(product):
    rating = Post.query.with_entities(func.avg(Post.rating).label('average')).filter_by(product=product)
    product.product_rating = rating
    db.session.commit()

def add_product_db(title, sterling, discounted_sterling, content, quantity):
    pro = Product(title=title, sterling=sterling, discounted_sterling=discounted_sterling, content=content, quantity=quantity)
    db.session.add(pro)
    db.session.commit()
    return pro

def add_picture(product, picture, alt):
    if picture:
        picture_file = save_picture(picture, "product_pics", size=(1000,1000))
        p_i = ProductImages(product_id=product.id, image_file=picture_file, alt=alt)
        db.session.add(p_i)
        db.session.commit()
        return True
    return False

def delete_product_db(product_id):
    pro = Product.query.get_or_404(product_id)
    images = ProductImages.query.filter(ProductImages.product_id==product_id)
    if images:
        for i in images:
            if i.image_file != 'default.png':
                path = os.path.join(current_app.root_path, 'static/product_pics', current_user.image_file)
                if os.path.exists(path):
                    os.remove(path)
            db.session.delete(i)
    #   relationship = ProductCategory.query.filter(ProductCategory.product_id==product_id)
 #   if relationship:
 #       for i in relationship:
 #           db.session.delete(i)
    db.session.delete(pro)
    db.session.commit()

def update_product_db(product, title, sterling, discounted_sterling, content, quantity):
    product.title=title
    product.sterling=sterling 
    product.discounted_sterling=discounted_sterling
    product.content=content
    product.quantity=quantity
    db.session.commit()

def add_category_db(name):
    cat = Category.query.get(name)
    if cat is None:
        cat = Category(category_name=name)
        db.session.add(cat)
        db.session.commit()
        return True
    return False

def delete_category_db(category_id):
    category = Category.query.get_or_404(category_id)
    if category:
  #      relationship = ProductCategory.query.filter(ProductCategory.category_id==category_id)
 #       if relationship:
  #          for i in relationship:
  #              db.session.delete(i)
        db.session.delete(category)
        db.session.commit()
        return True
    return False

def update_category_db(cat, name):
    cat.category_name = name
    db.session.commit()

def get_category(category_id):
    return Category.query.get_or_404(category_id)

def get_categories():
    return Category.query

def get_product_category(product_id):
    return ProductCategory.query.join(Category, Category.id==ProductCategory.category_id).add_columns(ProductCategory.id, ProductCategory.product_id).add_columns(Category.id, Category.category_name).filter(ProductCategory.product_id == product_id)

def add_product_category_db(product_id, category):
    pc = ProductCategory(product_id, category)
    db.session.add(pc)
    db.session.commit()

def delete_product_category(product_category_id):
    pc = ProductCategory.query.get_or_404(product_category_id)
    db.session.delete(pc)
    db.session.commit()
    return True

def register_user(username, email, hashed_password, address1, address2, city, country, postcode, phone):
    user = User(username=username, email=email, password=hashed_password, address1=address1, address2=address2, city=city, country=country, postcode=postcode, phone=phone)
    db.session.add(user)
    db.session.commit()

def get_user_db(email):
    return User.query.filter_by(email=email).first()

def get_user_db_username(username):
    return User.query.filter_by(username=username).first_or_404()

def add_profile_picture(picture):
    if picture:
        if current_user.image_file != 'default.jpg':
            path = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)
            if os.path.exists(path):
                os.remove(path)
        picture_file = save_picture(picture)
        current_user.image_file = picture_file

def update_account(username, email):
    current_user.username = username
    current_user.email = email
    db.session.commit()

def get_user_posts(user):
    return Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())

def add_cart_item(product_id, quantity):
    cart = get_cart_item(product_id)
    if cart:
        db.session.delete(cart)
    cart = Cart(current_user.id, product_id, quantity)
    db.session.add(cart)
    db.session.commit()

def get_products_in_cart():
    return Product.query.join(Cart, Product.id == Cart.product_id) \
        .add_columns(Product.id, Product.title, Product.discounted_sterling, Cart.quantity) \
        .add_columns(Product.discounted_sterling * Cart.quantity).filter(
        Cart.user_id == current_user.id)

def delete_from_cart_db(product_id):
    cart = get_cart_item(product_id)
    if cart:
        db.session.delete(cart)
        db.session.commit()

def modify_cart_db(product_id, amount):
    cart = get_cart_item(product_id)
    if cart:
        cart.quantity = cart.quantity + amount
        if cart.quantity <= 0:
            db.session.delete(cart)
        db.session.commit()

def handle_checkout(cc_number, cc_type):
    total_sum = calculate_total_price_with_tax(total_price())
    order = Order(total_price=total_sum, user_id=current_user.id)
    db.session.add(order)
    db.session.commit()
    sales_transaction = SaleTransaction(order_id=order.id, amount=total_sum, cc_number=cc_number, cc_type=cc_type, response="success")
    db.session.add(sales_transaction)
    db.session.commit()
    add_ordered_products(order.id)

def total_price():
    products_in_cart = Product.query.join(Cart, Product.id == Cart.product_id) \
        .add_columns(Product.discounted_sterling * Cart.quantity).filter(
        Cart.user_id == current_user.id)
    s = 0
    for row in products_in_cart:
        s += row[1]
  #  totalsum = float("%.2f" % (1.06 * float(totalsum)))
    return s

def calculate_total_price_with_tax(total_price):
    return float("%.2f" % (1.06 * float(total_price)))

def add_ordered_products(order_id):
    cart = get_cart_items()
    for i in cart:
        ordered_product = OrderedProduct(order_id=order_id, product_id=i.product_id, quantity=i.quantity)
        p = get_product(i.product_id)
        p.quantity = p.quantity-i.quantity
        db.session.add(ordered_product)
        db.session.delete(i)
        db.session.commit()

def has_access_level(access_level):
    if current_user.is_anonymous == False:
        r = Role.query.filter(Role.name == access_level).first()
        if r:
            user_role = UserRoles.query.filter(UserRoles.user_id == current_user.id).filter(UserRoles.role_id == r.id).first()
            if user_role:
                return True
    return False
