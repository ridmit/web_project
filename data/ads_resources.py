import os

from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.ads import Ad


class AdsResource(Resource):
    def get(self, ad_id):
        abort_if_ad_not_found(ad_id)
        session = db_session.create_session()
        ad = session.query(Ad).get(ad_id)
        return jsonify({'ad': ad.to_dict(
            only=('id', 'user_id', 'title', 'content', 'price', 'filename',
                  'created_date', 'is_sold'))})

    def delete(self, ad_id):
        abort_if_ad_not_found(ad_id)
        session = db_session.create_session()
        ad = session.query(Ad).get(ad_id)
        full_name = "static/img/" + ad.filename
        if os.path.exists(full_name):
            os.remove(full_name)
        session.delete(ad)
        session.commit()
        return jsonify({'success': 'OK'})


class AdsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        ads = session.query(Ad).all()
        return jsonify({'ads': [item.to_dict(
            only=('id', 'user_id', 'title', 'content', 'price', 'filename',
                  'created_date', 'is_sold')
        ) for item in ads]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        ad = Ad(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            price=args['price'],
            filename=args['filename'],
            is_sold=args['is_sold']
        )
        session.add(ad)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('price', required=True, type=int)
parser.add_argument('filename', required=True)
parser.add_argument('is_sold', required=True, type=bool)


def abort_if_ad_not_found(ad_id):
    session = db_session.create_session()
    ad = session.query(Ad).get(ad_id)
    if not ad:
        abort(404, message=f"Ad {ad_id} not found")
