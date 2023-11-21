from datetime import timedelta

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required

from laundry.auth import auth
from laundry.models import User



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user: User = User.query.filter_by(email=email).first()
        if user is None:
            flash('User does not exist', 'light-error')
            return redirect(url_for('.login'))
        elif not user.verify_password(password):
            flash('Incorrect password.', 'light-error')
            return redirect(url_for('.login'))
        # login existing user with provided correct password
        login_user(user, remember=True, duration=timedelta(days=30))
        # send admin to dashboard
        if user.is_superuser:
            next = url_for('admin.dashboard')
            return redirect(next)
        # send users to home page
        return redirect(url_for('main.profile'))
    return render_template('shared/login.html')


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
