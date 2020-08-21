from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DecimalField, RadioField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    sterling = DecimalField('Price', validators=[DataRequired()])
    discounted_sterling = DecimalField('Price Discounted', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    alt = StringField('Alt')
    picture = FileField('Add Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')

class CheckoutForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    address = TextAreaField('address', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired(), Length(min=2, max=20)])
    postcode = StringField('postcode', validators=[DataRequired(), Length(min=2, max=6)])
    cctype = RadioField('cardtype', choices=[('Visa','Visa'), ('Mastercard','Mastercard'), ('American Express','American Express'), ('Discover','Discover')], validators=[InputRequired()])
    cardname = StringField('cardnumber', validators=[DataRequired(), Length(min=12, max=12)])
    ccnumber = StringField('Credit card number', validators=[DataRequired()])
    expmonth = StringField('Exp Month', validators=[DataRequired()])
    expyear = StringField('Expiry Year', validators=[DataRequired(), Length(min=4, max=4)])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('MAKE PAYMENT')

class CategoryForm(FlaskForm):
    name = StringField('Category', validators=[InputRequired()])
    submit = SubmitField('Submit')

class ProductCategoryForm(FlaskForm):
    category = SelectField('Category', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Save')

class CartAddForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[NumberRange()])
    submit = SubmitField('Add to basket')
