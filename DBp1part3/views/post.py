from flask import Blueprint,flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from .test2 import auth

from DBp1part3 import sql
bp = Blueprint('post', __name__)

@bp.route('/create', methods=('GET', 'POST'))
@auth
def create():
    if request.method == 'POST':
        posted_at = request.form['posted_at']
        title = request.form['title']
        price = request.form['price']
        number = request.form['number']
        category = request.form['category']
        wantorsell = request.form['wantorsekk']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required.'
        if not price:
            error = 'Price is required.'
        if not wantorsell:
            error = 'Want it or need it?'
        if not number:
            error = 'Number is required.'
        if not category:
            error = 'Category is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO Items_Posted (posted_at, user_id, title, description, price, category, number, neededItem)'
                'VALUES (%D, %d, %s, %s, %f, %s, %d, %s)',
                (posted_at, Now(), session['user_id'], title, description, price, category, number, neededItem)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('create.html')