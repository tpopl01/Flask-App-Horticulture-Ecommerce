from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DecimalField, RadioField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Length


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    rating = SelectField('Rating', \
            choices=[('1','1 Star'), ('2','2 Star'), ('3','3 Star'), ('4','4 Star'), ('5','5 Star')], validators=[InputRequired()])
    submit = SubmitField('Post')

