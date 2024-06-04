from flask import Flask, render_template, redirect, url_for, flash, request, Blueprint
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from appDIS import bcrypt
from appDIS import roles,mysession
from appDIS import UserLoginForm, RegistrationForm
from appDIS import User, select_user, insert_user

Login = Blueprint('Login', __name__)

@Login.route("/")
@Login.route("/home")
def home():
    mysession["state"] = "home or /"
    role = mysession.get("role", None)
    return render_template('home.html', role=role)

@Login.route("/about")
def about():
    mysession["state"] = "about"
    return render_template('about.html', title='About')

@Login.route("/login", methods=['GET', 'POST'])
def login():
    mysession["state"] = "login"
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))

    is_bronze = request.args.get('is_bronze') == 'true'
    form = UserLoginForm()
    if form.validate_on_submit():
        user = select_user(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            mysession["role"] = user.role
            mysession["id"] = user.id
            flash('Login successful.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', form=form, role=mysession.get("role"))

@Login.route("/logout")
def logout():
    mysession["state"] = "logout"
    logout_user()
    return redirect(url_for('Login.home'))

@Login.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        insert_user(form.username.data, form.email.data, hashed_password, form.role.data)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('Login.login'))
    
    return render_template('register.html', form=form)

@Login.route("/account")
@login_required
def account():
    mysession["state"] = "account"
    role = mysession.get("role", None)
    # accounts = select_cus_accounts(current_user.get_id()) 
    return render_template('account.html', title='Account', role=role)

