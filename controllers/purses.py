from flask_restful import reqparse, Resource

from entities.purse import Purse

post_parser = reqparse.RequestParser()
post_parser.add_argument('total')
post_parser.add_argument('ccy')


class PursesController(Resource):

    @classmethod
    def apply_middleware(cls, api):
        api.add_resource(cls, '/purses')

    def post(self):
        return Purse(**post_parser.parse_args()).save().get_id()

    def get(self):
        return Purse.get_all()
