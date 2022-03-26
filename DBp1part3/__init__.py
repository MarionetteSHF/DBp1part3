from flask import Flask,render_template
from .views.login import auth
from DBp1part3.views.test2 import testblue2
from . import sql
from .views import post


DATA_dict = {
    '1':{'name': 'hanfu', 'age':25},
    '2':{'name': 'hanfu', 'age':52}
}

def create_app():
    app = Flask(__name__)
    app.secret_key='hanfushi'

    @app.route('/index')
    def index():
        rows = sql.fetchall('Items_Posted')
        return render_template('web/index.html', rows=rows)

    app.register_blueprint(auth)
    app.register_blueprint(testblue2)
    app.register_blueprint(post.bp)
    app.add_url_rule('/', endpoint='index')
    # app.register_blueprint(testblue, url_prefix ='/web')
    # app.register_blueprint(testblue2, url_prefix ='/admin')
    return app