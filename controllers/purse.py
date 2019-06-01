from flask import make_response
from flask_restful import Resource, reqparse
from entities.purse import Purse

storage = Purse.get_storage()

post_parser = reqparse.RequestParser()
post_parser.add_argument('total')
post_parser.add_argument('ccy')


class PurseController(Resource):

    @classmethod
    def apply_middleware(cls, api):
        api.add_resource(cls, '/purses/<string:purse_id>')

    def get(self, purse_id):
        return storage.create_json_response(storage.find_by_id(purse_id))

    def put(self, purse_id):
        return storage.create_json_response(storage.update_by_id(purse_id, post_parser.parse_args()))

    def delete(self, purse_id):
        return storage.create_json_response(storage.delete_by_id(purse_id))

