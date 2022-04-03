from flask import Flask, Blueprint,flash, g, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from .test2 import auth
from DBp1part3 import sql
import urllib.request
import os
from werkzeug.utils import secure_filename
from datetime import datetime

bp = Blueprint('post', __name__)
@bp.route('/create/<int:uid>', methods=('GET', 'POST'))
@auth
def create(uid):
    if request.method == 'POST':
        title = request.form['title']
        price = float(request.form['price'])
        number = int(request.form['number'])
        category = request.form['category']
        wantorsell = bool(request.form['wantorsell'])
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
            posted_at = datetime.now().strftime("%m/%d/%Y")
            cur.execute(
                'INSERT INTO Items_Posted (posted_at, user_id, title, description, item_id, price, category, number, neededItem)'
                'VALUES (%s, %s, %s, %s, default,%s, %s, %s, %s)',
                (posted_at, uid, title, description, price, category, number, wantorsell)
            )
            db.commit()
            db.close()
            return redirect(url_for('index'))
    return render_template('web/post.html')

def get_post(iid):
    db = sql.get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT *'
        ' FROM Items_Posted '
        ' WHERE item_id = %s',
        (iid,)
    )
    post = cur.fetchone()
    db.close()

    if post is None:
        abort(404, f"Post id {iid} doesn't exist.")

    return post


@bp.route('/update/<int:iid>', methods=('GET', 'POST'))
@auth
def update(iid):
    print(iid)
    post = get_post(iid)
    print(post[3])
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
                'UPDATE Items_Posted SET title = %s, price = %s, neededItem = %s, number = %s, category = %s'
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
    return render_template('web/profile.html', rows=rows,id=id,wishRows=wishRows)

@bp.route('/delete/<int:id>')
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
    db.commit()
    # rows = cur.fetchone()
    db.close()
    # print(rows)
    # flash("success")
    return redirect("/profile/"+str(session['user_id']))


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

# def insertBLOB(iid, photo):
#     db = sql.get_db()
#     cur = db.cursor()
#     sql_insert_blob_query = """ INSERT INTO Photos
#     (photo_id, item_id, photo) VALUES (default,%s,%s)"""
#
#     picture = convertToBinaryData(photo)
#     result = cur.execute(sql_insert_blob_query, (iid,picture))
#     db.commit()
#     db.close()
#     print("Image inserted successfully as a BLOB into table", result)
#
# UPLOAD_FOLDER = 'static/uploads/'
#
# bp.secret_key = "secret key"
# bp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# bp.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/', methods=['POST'])
def upload_image():
    db = sql.get_db()
    cursor = db.cursor()
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(bp.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)

        cursor.execute("INSERT INTO upload (title) VALUES (%s)", (filename,))
        db.commit()

        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return render_template('web/post.html')

@bp.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)