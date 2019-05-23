from flask import Flask
from flask_restful import Api

from controllers.purse import PurseController
from controllers.purses import PursesController

app = Flask(__name__)
api = Api(app)

PurseController.apply_middleware(api)
PursesController.apply_middleware(api)

if __name__ == '__main__':
    app.run(debug=True)
