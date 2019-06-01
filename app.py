from flask import Flask
from flask_restful import Api
from interface.interface import ConsoleInterface
from controllers.purse import PurseController
from controllers.purses import PursesController
import threading
import time


app = Flask(__name__)
api = Api(app)
PurseController.apply_middleware(api)
PursesController.apply_middleware(api)

def run_job():
    time.sleep(1)
    console_interface = ConsoleInterface()
    console_interface.console_init()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    t = threading.Thread(target=run_job)
    t.start()
    app.run(debug=False)
