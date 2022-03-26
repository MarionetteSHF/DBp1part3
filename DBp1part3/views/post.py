from flask import Blueprint,flash, g, redirect, render_template, request, url_for
from .test2 import auth
from DBp1part3 import sql
bp = Blueprint('post', __name__)
from datetime import datetime

@bp.route('/create/<int:uid>', methods=('GET', 'POST'))
@auth
def create(uid):
    if request.method == 'POST':
        posted_at = request.form['posted_at']
        title = request.form['title']
        price = request.form['price']
        number = request.form['number']
        category = request.form['category']
        wantorsell = request.form['wantorsell']
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
            db = sql.get_db()
            cur = db.cursor()
            create_at = cur.Column(db.DateTime, default=datetime.now)
            cur.execute(
                'INSERT INTO Items_Posted (posted_at, user_id, title, description, price, category, number, neededItem)'
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (posted_at, create_at, uid, title, description, price, category, number, wantorsell)
            )
            cur.commit()
            return redirect(url_for('index'))
    return render_template('post.html')

@bp.route('/<int:uid>/update', methods=('GET', 'POST'))
@auth
def update(uid):
    post = sql.get_db().cursor().execute(
        'SELECT p.user_id, title, description,  price, category, number, neededItem'
        ' FROM Items_Posted p JOIN Users u ON p.user_id = u.user_id'
        ' WHERE p.user_id = %s',
        (uid,)
    ).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        number = request.form['number']
        category = request.form['category']
        wantorsell = request.form['wantorsell']
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
            cur = sql.get_db().cursor()
            cur.execute(
                'UPDATE Items_Posted SET title = %s, price = %s, wantorsell = %s, number = %s, category = %s'
                ' WHERE user_id = ?',
                (title, price,wantorsell,number,category, uid)
            )
            cur.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


