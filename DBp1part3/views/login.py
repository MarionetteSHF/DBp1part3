from flask import Blueprint,request,session,redirect,render_template,url_for,flash
from werkzeug.security import check_password_hash, generate_password_hash
from DBp1part3 import sql
auth= Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form)
        email = request.form['email']
        password = request.form['pwd']

        db = sql.get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT encrypted_password,user_id  FROM Users WHERE email = %s",
            (email,),
        )
        rows = cur.fetchone()
        db.close()
        print(rows)
        error = None
        # print(rows[0])
        if rows is None:
            error = 'No such email.'+str(rows)
            return render_template('static/sign-in/login.html', error=error)


        elif not check_password_hash(rows[0], password):
            error = 'Incorrect password.'
            return render_template('static/sign-in/login.html', error=error)


        session['email']=email
        session['user_id'] = rows[1]
        print(session['user_id'])
        print(session['email'])
        return redirect('index')

        # return render_template('auth/login.html', error=error)
    else:
        return render_template('auth/sign-in.html')

        # return jsonify('data':1000)


@auth.route('/register', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        if "phone" in request.form:
            username = request.form['username']
            password = request.form['pwd']
            email = request.form['email']
            phone = request.form['phone']
            copy_pwd = request.form['copy_pwd']
            print(username +password+email+phone)
            db = sql.get_db()
            error = None

            if copy_pwd != password:
                error = 'please input same passwords'


            if error is None:
                try:
                    cur = db.cursor()

                    cur.execute(
                        "INSERT INTO Users (user_id, name, email, phone, encrypted_password  ) VALUES (default, %s, %s, %s, %s)",
                        (username,email,phone,generate_password_hash(password)),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"User {email} is already registered."
                else:
                    # flash(error)
                    # return render_template('auth/register/auth.html', error =error)
                    return redirect(url_for("auth.register"))
            print(error)
            db.close()
            flash(error)

            return render_template('auth/register/auth.html', error=error)
        else:
            email = request.form['email']
            password = request.form['pwd']

            db = sql.get_db()
            cur = db.cursor()
            cur.execute(
                "SELECT encrypted_password,user_id  FROM Users WHERE email = %s",
                (email,),
            )
            rows = cur.fetchone()
            db.close()
            print(rows)
            error = None
            # print(rows[0])
            if rows is None:
                error = 'No such email'
                return render_template('auth/register/auth.html', error=error)


            elif not check_password_hash(rows[0], password):
                error = 'Incorrect password.'
                return render_template('auth/register/auth.html', error=error)

            session['email'] = email
            session['user_id'] = rows[1]
            print(session['user_id'])
            print(session['email'])
            return redirect('index')








    return render_template('auth/register/auth.html')
    # return render_template('webpage/index_old.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))