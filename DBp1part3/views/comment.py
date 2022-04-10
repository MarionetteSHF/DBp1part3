from flask import Flask, Blueprint,flash, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from .test2 import auth
from DBp1part3 import sql
from datetime import datetime

comm = Blueprint('post', __name__)
@comm.route('/comment/<int:iid>', methods=('GET', 'POST'))
def comment(iid):
    if request.method == 'POST':
        comment_content = request.form['comment']
        db = sql.get_db()
        cur = db.cursor()
        comment_date = datetime.now().strftime("%m/%d/%Y")
        cur.execute(
            'INSERT INTO Comments (user_id, comment_id, item_id, comment_date, comment_content)'
            'VALUES (%s,default, %s, %s, %s)',
            (session["user_id"], iid, comment_date, comment_content)
        )
        db.commit()
        db.close()
    return render_template('webpage/display.html')