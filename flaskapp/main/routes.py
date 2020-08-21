from flask import render_template, request, Blueprint
from flaskapp.models import Product, ProductImages
from flaskapp.model_handling import get_products_with_image, get_products_with_image_of_cat, get_categories, has_access_level, has_products
from flaskapp.products.forms import ProductCategoryForm

main = Blueprint('main', __name__)


@main.route("/", methods=['GET','POST'])
@main.route("/home", methods=['GET','POST'])
def home():
    """Home Route."""
    form = ProductCategoryForm()
    categories = get_categories()
    groups_list=[]
    groups_list.append((-1, "All"))
    for i in categories:     
        groups_list.append((i.id, i.category_name))
    form.category.choices=groups_list
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        products = None
        if(has_products()):
            if(form.category.data == -1):
                products = get_products_with_image().paginate(page=page, per_page=8)
            else:
                products = get_products_with_image_of_cat(form.category.data).paginate(page=page, per_page=8)
        return render_template('home.html', products=products, form=form, admin=has_access_level("Admin"))
    products = None
    if(has_products()):
        products = get_products_with_image().paginate(page=page, per_page=8)
    return render_template('home.html', products=products, form=form, admin=has_access_level("Admin"))

@main.route("/about")
def about():
    """About Route."""
    return render_template('about.html', title='About')


