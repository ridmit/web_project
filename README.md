# Пояснительная записка

###1.Сайт по продаже изделий ручной работы

####https://sale-of-handmade-products.herokuapp.com/

###2.Неганов Дима

###3.На главной странице представлены объявления пользователей.
![0](https://user-images.githubusercontent.com/94733452/165831759-ce614359-60c0-461c-b540-7f0307712dd4.png)

Чтобы сделать своё объявление, необходимо зарегестрироваться и авторизироваться.

![1](https://user-images.githubusercontent.com/94733452/165831777-b05b37b7-0a6a-4bba-ba4e-224a29d03ef0.png)

После авторизации можно просмотреть свой профиль, отредактировать его, или выйти из аккаунта.
Также появляется кнопка добавления объявления

![2](https://user-images.githubusercontent.com/94733452/165831764-ae24220d-01d7-4c13-a7c3-868e4b4edd62.png)

Если объявление принадлежит текущему пользователю, то его можно изменить или удалить
Если же товар купили, то надо нажать кнопку на соотвествующем объявлении

![3](https://user-images.githubusercontent.com/94733452/165831769-7bdc77e8-36d3-40f9-8912-1badaf0f77c8.png)

Если кликнуть на какое-либо объявление, то отображается подробная информация о нём.

![4](https://user-images.githubusercontent.com/94733452/165831779-3eaeb331-3c44-47b5-94e5-6e1a4549f09e.png)

Можно просматривать так и свой профиль, так и аккаунты других пользователей.
В подробной информации об авторе можно увидеть все его объявления: как активные, так и завершённые.
![5](https://user-images.githubusercontent.com/94733452/165831772-869b4e41-5ce8-4f34-b609-f528f4075218.png)

###4.
В базе данных 2 таблицы: "users" и "ads"

Для регистрации и изменения профиля используется шаблон register.html

Для создания и редактирования объявления - ad.html

Для профиля используется шаблон profile.html

Главная страница - index.html

Все шаблоны унаследованы от base.html

Изображения хранятся в static/img

Кроме базы данных есть файл cities_utc.csv, 
в котором есть таблица крупнейших городов России с их utc

###5.Необходимые библиотеки

alembic

Flask

Flask-Login

Flask-RESTful

Flask-WTF


Jinja2

requests

SQLAlchemy

SQLAlchemy-serializer

Werkzeug

WTForms

####Главный файл – main.py
