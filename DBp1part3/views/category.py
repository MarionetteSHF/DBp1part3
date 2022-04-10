from flask import Flask, Blueprint,flash, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from DBp1part3 import sql
import urllib.request


ind = Blueprint('ind', __name__)
def categoryInd(kind):
    db = sql.get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT i.title, i.price,i.neededitem,i.item_id,p.image_source'
        ' FROM Items_Posted i, Photos p '
        ' WHERE i.item_id = p.item_id and category=%s'
        'ORDER BY i.posted_at DESC',
        (kind,)
    )
    rows = cur.fetchall()
    print(rows)
    db.close()
    return rows

@ind.route('/furniture')
def findex():
    rows = categoryInd('Furniture')
    return render_template('webpage/index.html', rows=rows)

@ind.route('/entertainment')
def eindex():
    rows = categoryInd('Entertainment')
    return render_template('webpage/index.html', rows=rows)
@ind.route('/book')
def bindex():
    rows = categoryInd('Book')
    return render_template('webpage/index.html', rows=rows)
@ind.route('/clothes')
def cindex():
    rows = categoryInd('Clothes')
    return render_template('webpage/index.html', rows=rows)

