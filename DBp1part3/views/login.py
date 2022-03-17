from flask import Blueprint,request,session,redirect,render_template

log= Blueprint('hf', __name__)


@log.route('/login', methods=['GET', 'POST'])
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
        return render_template('login.html')

        # return jsonify('data':1000)



