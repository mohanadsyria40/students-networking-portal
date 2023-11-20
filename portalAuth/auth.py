from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
        
    return render_template("login.html", boolean=True)


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        studentId = request.form.get('studentId')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(studentId) < 9:
            flash('Student ID must be 9 characters! ', category='error')
        elif len(firstname) < 2:
            flash('First name must consist of at least 2 characters! ', category='error')
        elif len(lastname) < 2:
            flash('Last name must consist of at least 2 characters! ', category='error')
        elif len(email) < 10:
            flash('Email must consist of at least 10 characters! ', category='error')
        elif len(password1) < 2:
            flash('Password must be more than 2 characters! ', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match! ', category='error')
        else:
            # add student to the database
            flash('Account is successfully created ', category='success')
    return render_template("sign_up.html")