import os

from random import randint
from datetime import datetime
from flask import Flask, render_template, redirect, abort, request, \
    jsonify, make_response
from flask_restful import abort, Api
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user
from werkzeug.utils import secure_filename

from data import db_session, ads_resources
from data.ads import Ad
from data.users import User
from forms.ad import AdForm, AdEditForm, materials
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/<city>/<material>")
def index(city="Любой город", material="Любой материал"):
    db_sess = db_session.create_session()
    filters = [Ad.is_sold == 0]
    if city != "Любой город":
        filters.append(User.city == city)
    if material != "Любой материал":
        filters.append(Ad.material == material)
    ads = db_sess.query(Ad).join(User).filter(*filters).all()

    cities = set([user.city for user in db_sess.query(User).all()])
    params = {
        "cities": cities,
        "current_city": city,
        "materials": materials[:-1],
        "current_material": material,
        "ads": ads,
        "css": "../static/css/index.css",
        "title": "Продажа изделий ручной работы"
    }
    return render_template("index.html", **params)


@app.route("/user/<user_id>/<state>")
def profile(user_id, state):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    active_ads = db_sess.query(Ad).filter(Ad.user == user,
                                          Ad.is_sold == 0).all()
    complete_ads = db_sess.query(Ad).filter(Ad.user == user,
                                            Ad.is_sold == 1).all()
    ads = complete_ads if state == "complete" else active_ads
    params = {
        "user": user,
        "ads": ads,
        "active": active_ads,
        "complete": complete_ads,
        "title": f"Профиль пользователя {user.name} {user.surname}",
        "state": state,
        "css": "/static/css/index.css"
    }
    return render_template("profile.html", **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            patronymic=form.patronymic.data,
            city=form.city.data.lower().capitalize(),
            age=form.age.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/ad', methods=['GET', 'POST'])
@login_required
def add_ad():
    form = AdForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ad = Ad()
        ad.title = form.title.data
        ad.content = form.content.data
        ad.condition = form.condition.data
        ad.price = form.price.data
        ad.material = form.material.data
        f = form.image.data
        # в конец названия изображения добавляется случайно число, чтобы
        # в базу данных не попали фотографии с одинаковым названием
        rand_num = randint(10 ** 5, 10 ** 6 - 1)
        filename = secure_filename(
            (str(rand_num) + '.').join(f.filename.split('.')))
        f.save(os.path.join("static/img", filename))
        ad.filename = filename
        current_user.ads.append(ad)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('ad.html', title='Добавление объявления',
                           form=form)


@app.route('/ad/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ad(id):
    form = AdEditForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        ad = db_sess.query(Ad).filter(Ad.id == id,
                                      Ad.user == current_user).first()
        if ad:
            form.title.data = ad.title
            form.content.data = ad.content
            form.price.data = ad.price
            form.material.data = ad.material
            form.condition.data = ad.condition
            form.current_img.data = f"../static/img/{ad.filename}"
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ad = db_sess.query(Ad).filter(Ad.id == id,
                                      Ad.user == current_user).first()
        if ad:
            ad.title = form.title.data
            ad.content = form.content.data
            ad.price = form.price.data
            ad.material = form.material.data
            ad.condition = form.condition.data
            ad.created_date = datetime.now()
            f = form.image.data
            if f:
                full_name = "static/img/" + ad.filename
                if os.path.exists(full_name):
                    os.remove(full_name)
                rand_num = randint(10 ** 5, 10 ** 6 - 1)
                filename = secure_filename(
                    (str(rand_num) + '.').join(f.filename.split('.')))
                f.save(os.path.join("static/img", filename))
                ad.filename = filename
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('ad.html',
                           title='Редактирование объявления',
                           form=form)


@app.route('/change_is_sold/<int:param>/<int:id>', methods=['GET', 'POST'])
@login_required
def change_is_sold(param, id):
    db_sess = db_session.create_session()
    ad = db_sess.query(Ad).filter(Ad.id == id,
                                  Ad.user == current_user).first()
    if ad:
        ad.is_sold = param
        db_sess.commit()
    else:
        abort(404)
    if param == 1:
        return redirect(f"/user/{current_user.id}/complete")
    return redirect('/')


@app.route('/ad_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def ad_delete(id):
    db_sess = db_session.create_session()
    ad = db_sess.query(Ad).filter(Ad.id == id,
                                  Ad.user == current_user).first()
    if ad:
        db_sess.delete(ad)
        db_sess.commit()
        full_name = "static/img/" + ad.filename
        if os.path.exists(full_name):
            os.remove(full_name)
    else:
        abort(404)
    return redirect('/')


@app.route("/ad/details/<int:ad_id>")
def ad_details(ad_id):
    db_sess = db_session.create_session()
    ad = db_sess.query(Ad).filter(Ad.id == ad_id).first()
    return render_template("ad_details.html", ad=ad,
                           title=f"Обзор товара")


def main():
    db_session.global_init("db/database.db")

    # для списка объектов
    api.add_resource(ads_resources.AdsListResource, '/api/ads')
    # для одного объекта
    api.add_resource(ads_resources.AdsResource, '/api/ads/<int:ad_id>')

    app.run()


if __name__ == '__main__':
    main()
