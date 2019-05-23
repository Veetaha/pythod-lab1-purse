from flask_restful import Resource
from entities.purse import Purse


class PurseController(Resource):

    @classmethod
    def apply_middleware(cls, api):
        api.add_resource(cls, '/purses/<string:purse_id>')

    def get(self, purse_id):
        purse = Purse.find_by_id(purse_id)
        if purse is not None:
            return purse.to_json()
        else:
            return None, 404

    def delete(self, purse_id):
        return Purse.delete()

