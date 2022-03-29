from data import db_session
from data.ads import Ad
from data.users import User


def select_all_users(db_sess):
    for user in db_sess.query(User).all():
        print("; ".join(map(str, [user.id, user.name,
                                  user.surname, user.patronymic,
                                  user.city, user.age,
                                  user.email, user.about,
                                  user.created_date])))


def select_all_ads(db_sess):
    for ad in db_sess.query(Ad).all():
        print("; ".join(map(str, [ad.id, ad.user_id, ad.title,
                                  ad.content, ad.price,
                                  ad.filename, ad.created_date,
                                  ad.is_sold])))


if __name__ == '__main__':
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()
    select_all_users(db_sess)
    select_all_ads(db_sess)
