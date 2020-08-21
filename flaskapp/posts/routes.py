from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import Post, Product, Cart, ProductCategory, Category, Order, SaleTransaction, UserRoles, Role, OrderedProduct
from flaskapp.posts.forms import PostForm
from flaskapp.products.forms import CartAddForm, ProductForm, CheckoutForm
from flaskapp.model_handling import delete_comment, get_comment, update_comment, create_comment

posts = Blueprint('posts', __name__)


#@posts.route("/post/new", methods=['GET', 'POST'])
#@login_required
#def new_post():
 #   form = PostForm()
 #   if form.validate_on_submit():
 #       create_comment(title=form.title.data, content=form.content.data, author=current_user)
 #       flash('Your post has been created!', 'success')
 #       return redirect(url_for('main.home'))
 #   return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = get_comment(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = get_comment(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        update_comment(post, form.title.data, form.content.data, form.rating.data)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.rating.data = post.rating
        form.rating.process_data(post.rating)
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    delete_comment(post_id)
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('main.home'))

