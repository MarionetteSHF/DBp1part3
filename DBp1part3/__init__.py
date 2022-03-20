from flask import Flask,render_template
from .views.login import log
from .views.test2 import testblue2
from .views import  sql
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

        return render_template('index.html', rows=rows)
        # return  str(rows[0][0])

    app.register_blueprint(log)
    app.register_blueprint(testblue2)
    # app.register_blueprint(testblue, url_prefix ='/web')
    # app.register_blueprint(testblue2, url_prefix ='/admin')
    return app