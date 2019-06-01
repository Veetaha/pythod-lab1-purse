import schema
import json

from flask import make_response
from flask_restful import reqparse, Resource

from entities.purse import Purse

post_parser = reqparse.RequestParser()
post_parser.add_argument('total')
post_parser.add_argument('ccy')

storage = Purse.get_storage()


class PursesController(Resource):

    @classmethod
    def apply_middleware(cls, api):
        api.add_resource(cls, '/purses')

    def post(self):
        try:
            return {"id": storage.insert(Purse(post_parser.parse_args())).id}, 200
        except:
            return {"error": "Invalid parameters"}, 400

    def get(self):
        return storage.create_json_response(list(storage.get_all().values()))
