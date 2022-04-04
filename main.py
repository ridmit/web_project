import os

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user
from werkzeug.utils import secure_filename

from data import db_session
from data.ads import Ad
from data.users import User
from forms.ad import AdForm
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    ads = db_sess.query(Ad).filter(Ad.is_sold == 0)
    return render_template("index.html", ads=ads)


@app.route("/user/<user_id>")
def profile(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    return render_template("profile.html", user=user)


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
            city=form.city.data,
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
def add_news():
    form = AdForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ad = Ad()
        ad.title = form.title.data
        ad.content = form.content.data
        ad.price = form.price.data
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join("static\\img", filename))
        ad.filename = filename
        current_user.ads.append(ad)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('ad.html', title='Добавление объявления',
                           form=form)


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()
