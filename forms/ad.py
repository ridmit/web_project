from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField, \
    SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired

kinds = ["Изделие из дерева", "Изделие из кожи",
         "Изделие из природных материалов", "Изделие из ткани",
         "Изделие из бисера", "Рисунок", "Другое"]


class AdForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    material = SelectField("Вид изделия",
                           choices=kinds, validators=[DataRequired()])
    price = IntegerField("Цена", validators=[DataRequired()])
    image = FileField("Изображение", validators=[DataRequired()])
    current_img = StringField()
    submit = SubmitField("Подтвердить")


class AdEditForm(AdForm):
    image = FileField("Изменить изображение")
