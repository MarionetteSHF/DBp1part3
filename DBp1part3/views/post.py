from flask import Blueprint,flash, g, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
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
                'INSERT INTO Items_Posted (posted_at, user_id, title, description, item_id, price, category, number, neededItem)'
                'VALUES (%s, %s, %s, %s, %s, default, %s, %s, %s)',
                (posted_at, create_at, uid, title, description, price, category, number, wantorsell)
            )
            db.commit()
            db.close()
            return redirect(url_for('index'))
    return render_template('web/post.html')

def get_post(iid):
    post = sql.get_db().cursor().execute(
        'SELECT *'
        ' FROM Items_Posted p '
        ' WHERE p.item_id = %s',
        (iid,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {iid} doesn't exist.")

    return post


@bp.route('/update/<int:iid>', methods=('GET', 'POST'))
@auth
def update(iid):
    post = get_post(iid)
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
            db = sql.get_db()
            cur = db.cursor()
            cur.execute(
                'UPDATE Items_Posted SET title = %s, price = %s, wantorsell = %s, number = %s, category = %s'
                ' WHERE item_id = %s',
                (title, price,wantorsell,number,category, iid)
            )
            db.commit()
            db.close()
            return redirect(url_for('index'))

    return render_template('web/update.html', post=post)




@bp.route('/display/<int:id>')
@auth
def display(id):
    db = sql.get_db()
    print(id)
    cur = db.cursor()
    cur.execute(
        "SELECT *  FROM Items_Posted WHERE item_id = %s",
        (id,),
    )
    rows = cur.fetchone()
    db.close()
    print(rows)
    return render_template('web/display.html', row = rows)
    # redirect()

@bp.route('/profile/<int:id>')
@auth
def profile(id):
    db = sql.get_db()
    print(id)
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM Items_Posted WHERE User_id = %s",
        (id,),
    )
    rows = cur.fetchall()
    cur.execute(
        "SELECT * FROM Whishlists_Create_add WHERE User_id = %s",
        (id,),
    )
    wishRows = cur.fetchall()
    db.close()
    print(rows)
    return render_template('web/profile.html', row=rows,id=id,wishRows=wishRows)

@bp.route('/delete/<int:id>', methods=('POST',))
@auth
def delete(id):
    get_post(id)
    db = sql.get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM Items_Posted WHERE item_id = %', (id,))
    db.commit()
    db.close()
    return redirect(url_for('index'))
    return render_template('web/profile.html', row=rows)

@bp.route('/addtowish/<int:iid>')
def add_to_wishlist(iid):
    db = sql.get_db()
    print(iid)
    cur = db.cursor()
    cur.execute(
        "INSERT INTO Whishlists_Create_add (list_id, user_id, item_id  ) VALUES (default, %s, %s)",
        (session['user_id'], iid),
    )
    # rows = cur.fetchone()
    db.close()
    # print(rows)
    flash("success")
    return redirect("/index")