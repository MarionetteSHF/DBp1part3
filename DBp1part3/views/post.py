from flask import Blueprint,flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from .login import auth
from DBp1part3 import sql
bp = Blueprint('post', __name__)

@bp.route('/')
def index():
    db = sql.get_db().cursor()
    db.execute(
        'SELECT posted_at, p.user_id, title, description, price, category,neededItem, u.name'
        ' FROM Items_Posted p JOIN Users u ON p.user_id = u.user_id'
        ' ORDER BY posted_at DESC'
    )
    posts=db.fetchall()
    return render_template('web/post/index.html', posts=posts)