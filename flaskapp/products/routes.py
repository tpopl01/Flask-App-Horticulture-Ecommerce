from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import Post, Product, Cart, ProductCategory, Category, Order, SaleTransaction, UserRoles, Role, OrderedProduct, ProductImages
from flaskapp.posts.forms import PostForm
from flaskapp.products.forms import CartAddForm, ProductForm, CheckoutForm
from flaskapp.model_handling import handle_checkout, modify_cart_db, delete_from_cart_db, get_product, get_product_posts, get_product_images, get_orders, get_cart_items, get_cart_item, create_comment, add_cart_item, get_products_in_cart

products = Blueprint('products', __name__)

@products.route("/product/<int:product_id>", methods=['GET', 'POST'])
def product(product_id):
    page = request.args.get('page', 1, type=int)
    p = get_product(product_id)
    posts = get_product_posts(p).paginate(page=page, per_page=5)
    images = get_product_images(product_id).limit(6)
    if images is None:
        images = []
        images.append(ProductImages(product_id=product_id, image_file='default.jpg', alt='default'))
    count = images.count()
    form = PostForm()
    form1 = CartAddForm()
    if form.validate_on_submit() and request.method=='POST':
        create_comment(title=form.title.data, content=form.content.data, rating=form.rating.data, author=current_user, product=p)
        flash('Your post has been created!', 'success')
      #  posts = get_product_posts(product).paginate(page=page, per_page=5)
        return redirect(url_for('products.product', product_id=product_id))#render_template('product.html', product=p, posts=posts, form=form, form1=form1, images=images, count=count)
       # return render_template('product.html', product=product, posts=posts, title='Comments', form=form, form1=form1, legend='Comments')
    elif current_user.is_authenticated:
        if form1.validate_on_submit():
            if form1.quantity.data > p.quantity or form1.quantity.data < 1:
                flash('Quantity must be between 1 and ' + str(p.quantity), 'warning')
                return render_template('product.html', product=p, posts=posts, form=form, form1=form1, images=images, count=count)
            add_cart_item(product_id, form1.quantity.data)
            flash('Your item has been added to the cart!', 'success')
         #   posts = get_product_posts(product).paginate(page=page, per_page=5)
            return redirect(url_for('products.product', product_id=product_id))#return render_template('product.html', product=p, posts=posts, form=form, form1=form1, images=images, count=count)
           # return render_template('product.html', product=product, posts=posts, form=form, form1=form1, images=images, count=count)
    return render_template('product.html', product=p, posts=posts, form=form, form1=form1, images=images, count=count)

@products.route("/cart", methods=['GET', 'POST'])
@login_required
def cart():
    products_in_cart = get_products_in_cart()
    return render_template('cart.html', products_in_cart=products_in_cart)

@products.route("/cart/<int:product_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_from_cart(product_id):
    delete_from_cart_db(product_id)
    return redirect(url_for('products.cart'))

@products.route("/cart/<int:product_id>/add", methods=['GET', 'POST'])
@login_required
def increase_cart_product(product_id):
    modify_cart_db(product_id, 1)
    return redirect(url_for('products.cart'))

@products.route("/cart/<int:product_id>/reduce", methods=['GET', 'POST'])
@login_required
def reduce_cart_product(product_id):
    modify_cart_db(product_id, -1)
    return redirect(url_for('products.cart'))

#@products.route("/category/<int:category_id>", methods=['GET'])
#def displayCategory(category_id):
#    products_category = Product.query.join(ProductCategory, Product.id == ProductCategory.product_id)\
#        .add_columns(Product.id, Product.product_name, Product.discounted_sterling).filter(ProductCategory.category_id == category_id)
    
#    return render_template('category.html', products_category=products_category)

@products.route("/checkout", methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        print(form.cctype.data)
        handle_checkout(form.ccnumber.data, form.cctype.data)
        return redirect(url_for('products.orders'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.address.data = current_user.address1
        form.city.data = current_user.city
        form.postcode.data = current_user.postcode
    return render_template('checkout.html', form=form)

@products.route("/orders", methods=['GET'])
@login_required
def orders():
    return render_template('orders.html', orders=get_orders())



