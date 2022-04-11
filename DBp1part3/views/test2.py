from flask import Blueprint,request,session,redirect,url_for
import functools
testblue2 = Blueprint('hs', __name__)

DATA_dict = {
    '1':{'name': 'hanfu', 'age':25},
    '2':{'name': 'hanfu', 'age':52}
}
def auth(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        username = session.get('user_id')
        if not username:
            return redirect('/index')

        return func(*args, **kwargs)
    return inner

@testblue2.route("/edit")
@auth
def edit():
    nid = request.args.get('nid')
    print(nid)
    return "edit"

@testblue2.route("/del/<int:nid>")
@auth
def delete(nid):
    del DATA_dict[str(nid)]

    # return redirect('/index')
    return redirect('/index')#anotrher name of index
    # return render_template('index_old.html', data_dict=DATA_dict)