from flask import Blueprint

testblue2 = Blueprint('hs', __name__)

@testblue2.route('/f3')
def f1():
    return 'xf1'

@testblue2.route('/f4')
def f2():
    return 'xf2'