from flask import Flask, Blueprint,flash, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from .test2 import auth
from DBp1part3 import sql
import urllib.request
from io import BytesIO,StringIO
import base64
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
        wantorsell = True if request.form['wantorsell'] == 'need' else False
        description = request.form['description']
        error = None

        print(category)
        print(wantorsell)

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
    return render_template('webpage/post.html')

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

def get_pic(iid):
    db = sql.get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT photo_id,image_source FROM Photos WHERE item_id = %s',
        (iid,)
    )
    img_stream_file = cur.fetchall()
    db.close()
    return img_stream_file

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @bp.route('/update/<int:iid>', methods=('GET', 'POST'))
@bp.route('/update/<int:iid>/<int:uid>', methods=('GET', 'POST'))
@auth
def update(iid,uid):
    if session["user_id"] !=uid:
        return redirect(url_for('post.profile', id=session["user_id"]))

    post = get_post(iid)
    image_file = get_pic(iid)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        number = request.form['number']
        category = request.form['category']
        wantorsell = True if request.form['wantorsell'] == 'need' else False
        file = request.files['file']

        error = None


        if error is not None:
            flash(error)
        else:
            db = sql.get_db()
            cur = db.cursor()
            cur.execute(
                'UPDATE Items_Posted SET title = %s, price = %s, neededItem = %s, number = %s, category = %s,description=%s'
                ' WHERE item_id = %s',
                (title, price,wantorsell,number,category, description,iid)
            )
            db.commit()
            if file and allowed_file(file.filename):
                img_stream = file.read()

                img_stream = base64.b64encode(img_stream).decode()

                cur.execute("INSERT INTO Photos (photo_id, item_id, image_source) VALUES (default,%s,%s)",
                               (iid, img_stream,))
                db.commit()
                db.close()
                flash('Image successfully uploaded and displayed above')

            else:
                flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(url_for('post.update',iid=iid, uid=session["user_id"]))

    return render_template('webpage/update.html', post=post,file=image_file)


@bp.route('/display/<int:iid>',methods=('GET', 'POST'))
@auth
def display(iid):
    db = sql.get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT i.*, u.name, u.email,u.phone FROM Items_Posted i,Users u  WHERE item_id = %s",
        (iid,),
    )
    row = cur.fetchone()
    cur.execute(
        "SELECT image_source FROM Photos WHERE item_id = %s",
        (iid,),
    )
    img_stream_file = cur.fetchall()
    cur.execute(
        "SELECT u.name, c.comment_content,c.comment_date  FROM Comments c,Users u WHERE c.user_id=u.user_id and item_id = %s",
        (iid,),
    )
    comms = cur.fetchall()
    if request.method == 'POST':
        comment_content = request.form['comment']
        comment_date = datetime.now().strftime("%m/%d/%Y")
        cur.execute(
            'INSERT INTO Comments (user_id, comment_id, item_id, comment_date, comment_content)'
            'VALUES (%s,default, %s, %s, %s)',
            (session["user_id"], iid, comment_date, comment_content)
        )
        db.commit()
        db.close()
        return redirect(url_for('post.display', iid=iid))
    return render_template('webpage/display.html', row = row, file=img_stream_file,comms=comms)



@bp.route('/profile/<int:id>')
@auth
def profile(id):
    if session["user_id"] != id:
        return redirect(url_for('post.profile', id=session["user_id"]))
    db = sql.get_db()
    print(id)
    cur = db.cursor()
    cur.execute(
        "SELECT title,price,neededItem,item_id FROM Items_Posted WHERE User_id = %s",
        (id,),
    )
    rows = cur.fetchall()
    cur.execute(
        "SELECT i.title,i.price, u.name,u.phone,w.list_id FROM Whishlists_Create_add w, Items_Posted i, Users u WHERE w.item_id=i.item_id and i.User_id=u.User_id and w.User_id = %s",
        (id,),
    )
    wishRows = cur.fetchall()
    db.close()

    return render_template('webpage/profile.html', rows=rows,id=id,wishRows=wishRows)

@bp.route('/imageDelete/<int:pid>')
def imageDelete(pid):
    db = sql.get_db()
    cur = db.cursor()
    cur.execute('SELECT item_id FROM Photos WHERE photo_id = %s', (pid,))
    iid=cur.fetchone()
    cur.execute('DELETE FROM Photos WHERE photo_id = %s', (pid,))
    db.commit()
    db.close()
    return redirect(url_for('post.update',iid=iid,uid=session["user_id"]))

@bp.route('/itemDelete/<int:iid>')
def itemDelete(iid):
    db = sql.get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM Items_Posted WHERE item_id = %s', (iid,))
    db.commit()
    db.close()
    return redirect(url_for('post.profile', id=session["user_id"]))

@bp.route('/wishDelete/<int:lid>')
def wishDelete(lid):
    db = sql.get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM Whishlists_Create_add WHERE list_id = %s', (lid,))
    db.commit()
    db.close()
    return redirect(url_for('post.profile', id=session["user_id"]))

@bp.route('/addtowish/<int:iid>')
def add_to_wishlist(iid):
    db = sql.get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO Whishlists_Create_add (list_id, user_id, item_id  ) VALUES (default, %s, %s)",
        (session['user_id'], iid),
    )
    db.commit()
    db.close()
    return redirect(url_for('post.display', iid=iid))



