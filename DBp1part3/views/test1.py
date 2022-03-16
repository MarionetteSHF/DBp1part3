from flask import Blueprint

testblue = Blueprint('hf', __name__)

@testblue.route('/f1')
def f1():
    return 'f1'

@testblue.route('/f2')
def f2():
    return 'f2'

