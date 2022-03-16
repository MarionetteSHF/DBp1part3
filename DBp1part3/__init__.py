from flask import Flask
from .views.test1 import testblue
from .views.test2 import testblue2
def create_app():
    app = Flask(__name__)
    app.secret_key='hanfushi'

    @app.route('/index')
    def index():
        return 'index'

    app.register_blueprint(testblue)
    app.register_blueprint(testblue2)
    # app.register_blueprint(testblue, url_prefix ='/web')
    # app.register_blueprint(testblue2, url_prefix ='/admin')
    return app