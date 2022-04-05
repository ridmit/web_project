import os

from flask import jsonify
from flask_restful import abort, Resource

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


def abort_if_ad_not_found(ad_id):
    session = db_session.create_session()
    ad = session.query(Ad).get(ad_id)
    if not ad:
        abort(404, message=f"Ad {ad_id} not found")
