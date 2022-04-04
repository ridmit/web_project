from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class AdForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    price = IntegerField("Цена", validators=[DataRequired()])
    image = FileField("Изображение", validators=[DataRequired()])
    submit = SubmitField("Создать")
