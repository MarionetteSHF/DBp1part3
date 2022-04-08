from flask import Flask, Blueprint,flash, redirect, render_template, request, url_for,session
from werkzeug.exceptions import abort
from DBp1part3 import sql
import urllib.request


ind = Blueprint('ind', __name__)
def categoryInd(kind):
    db = sql.get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT *'
        ' FROM Items_Posted '
        ' WHERE category=%s',
        (kind,)
    )
    rows = cur.fetchall()
    print(rows)
    db.close()
    return render_template('webpage/index.html', rows=rows)

@ind.route('/furniture')
def findex():
    return categoryInd('furniture')
@ind.route('/entertainment')
def eindex():
    return categoryInd('entertainment')
@ind.route('/book')
def bindex():
    return categoryInd('book')
@ind.route('/clothe')
def cindex():
    return categoryInd('clothe')

