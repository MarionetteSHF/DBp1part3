from flask import Blueprint,request,session,redirect,render_template,url_for,flash
from werkzeug.security import check_password_hash, generate_password_hash
from DBp1part3 import sql
auth= Blueprint('hf', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        user = request.form.get('username')
        pwd = request.form.get('pwd')
        if user == 'x11' and pwd == 'y':
            session['xxx']='x11'
            return redirect('/index')
        error = 'no such user or pwd is wrong'
        return render_template('login.html', error=error)
    else:
        return render_template('auth/login.html')

        # return jsonify('data':1000)


@auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sql.get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template('auth/register.html')
