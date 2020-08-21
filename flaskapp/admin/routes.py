from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import Post, Product, Cart, ProductCategory, Category, Order, SaleTransaction, UserRoles, Role, OrderedProduct, ProductImages
from flaskapp.posts.forms import PostForm
from flaskapp.products.forms import CartAddForm, ProductForm, CheckoutForm, CategoryForm, ProductCategoryForm
from flaskapp.decorators.decorators import roles_required
from flaskapp.users.utils import save_picture
from flaskapp.model_handling import delete_product_category, add_product_category_db, get_product_category, get_categories, get_product, get_products_with_image, add_picture, add_product_db, delete_product_db, update_product_db, add_category_db, delete_category_db, update_category_db, get_category, has_products

admin = Blueprint('admin', __name__)

#ADMIN ONLY
@admin.route("/admin/product", methods=['GET','POST'])
@roles_required('Admin')
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        pro = add_product_db(title=form.title.data, sterling=form.sterling.data, discounted_sterling=form.discounted_sterling.data, content=form.content.data, quantity=form.quantity.data)
        if add_picture(pro, form.picture.data, form.alt.data):
            flash('Picture Added!', 'success')
        flash('Your product has been created!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('create_product.html', title='New Product', form=form, legend='New Product')

@admin.route("/admin/product/<int:product_id>/delete", methods=['GET', 'POST'])
@roles_required('Admin')
def delete_product(product_id):
    delete_product_db(product_id)
    flash('Your product has been deleted!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin.route("/admin/product/<int:product_id>/update", methods=['GET', 'POST'])
@roles_required('Admin')
def update_product(product_id):
    pro = Product.query.get_or_404(product_id)
    form = ProductForm()
    if form.validate_on_submit():
        if add_picture(pro, form.picture.data, form.alt.data):
            flash('Picture Added!', 'success')
        update_product_db(pro, form.title.data, form.sterling.data, form.discounted_sterling.data, form.content.data, form.quantity.data)
        flash('Your product has been updated!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    elif request.method == 'GET':
        form.title.data = pro.title
        form.sterling.data = pro.sterling
        form.discounted_sterling.data = pro.discounted_sterling
        form.content.data = pro.content
        form.quantity.data = pro.quantity
    return render_template('create_product.html', title='Modify Product', form=form, legend='Modify Product')

@admin.route("/admin/category", methods=['GET','POST'])
@roles_required('Admin')
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        if add_category_db(form.name.data):
            flash('Your category has been created!', 'success')
            return redirect(url_for('admin.categories'))
        else:
            flash('Category already exists!', 'danger')
    return render_template('create_category.html', title='New Category', form=form, legend='New Category')

@admin.route("/admin/categories", methods=['GET','POST'])
@roles_required('Admin')
def categories():
    page = request.args.get('page', 1, type=int)
    categories = get_categories().paginate(page=page, per_page=5)
    return render_template('categories.html', categories=categories)

@admin.route("/admin/category/<int:category_id>/delete", methods=['GET', 'POST'])
@roles_required('Admin')
def remove_category(category_id):
    if delete_category_db(category_id):
        flash('Your category has been deleted!', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('home.html')

@admin.route("/admin/category/<int:category_id>/update", methods=['GET', 'POST'])
@roles_required('Admin')
def update_category(category_id):
    cat = get_category(category_id)
    form = CategoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        update_category_db(cat,form.name.data)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('admin.categories'))
    elif request.method == 'GET':
        form.name.data = cat.category_name
    return render_template('create_category.html', title='Update Category', form=form, legend='Update Category')

@admin.route("/admin/product_category/<int:product_id>")
@roles_required('Admin')
def product_category(product_id):
    pc = get_product_category(product_id)
    product = get_product(product_id)
    return render_template('product_categories.html', pc=pc, product_id=product_id, product=product)

@admin.route("/admin/product_category/<int:product_id>/add", methods=['GET', 'POST'])
@roles_required('Admin')
def add_product_category(product_id):
    form = ProductCategoryForm()
    product = get_product(product_id)
    categories = get_categories().all()
    if len(categories) ==0:
        flash('Set up a category first!', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    groups_list=[(i.id, i.category_name) for i in categories]
    form.category.choices=groups_list
    if form.validate_on_submit():
        add_product_category_db(product_id, form.category.data)
        flash('Your product-category relationship has been created!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('create_product_category.html', title='New Product Category', form=form, legend='New Product Category', product=product)

@admin.route("/admin/product_category/<int:product_category_id>/delete", methods=['GET', 'POST'])
@roles_required('Admin')
def remove_product_category(product_category_id):
    if delete_product_category(product_category_id):
        flash('Your product-category relationship has been deleted!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('home.html')

@admin.route("/admin/dashboard", methods=['GET', 'POST'])
@roles_required('Admin')
def admin_dashboard():
    page = request.args.get('page', 1, type=int)
    products = None
    if(has_products()):
        products = get_products_with_image().paginate(page=page, per_page=8)
    return render_template('dashboard_admin.html', products=products)
