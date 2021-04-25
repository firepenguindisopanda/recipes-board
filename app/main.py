import json
from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
from sqlalchemy.exc import IntegrityError
import os
from flask_jwt import JWT, jwt_required, current_identity
from flask_login import UserMixin
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

#models
from .models import db, Recipe, Ingredient, User, UserRecipe
from app import app
from .forms import LogIn, SignUp
from . import login_manager

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', data = recipes)

@app.route('/login')
def loginPAge():
    form = LogIn()
    return render_template('login.html', form=form)

@app.route('/signup')
def signupPage():
    form = SignUp()
    return render_template('/signup.html', form=form)

@app.route('/login', methods=['POST'])
def loginFunction():
    form = LogIn()
    if form.validate_on_submit():
        info = request.form
        user = User.query.filter_by(username = info['username']).first()
        if user and user.check_password(info['password']):
            login_user(user)
            print('Loggin in as ' + info['username'])
            return redirect(url_for('index'))
    flash('Invalid login info')
    print('Invalid login info')
    return redirect(url_for('loginPAge'))

@app.route('/signup', methods=['POST'])
def signupFunction():
    form = SignUp()
    if form.validate_on_submit():
        info = request.form
        newUser = User(username=info['username'], email = info['email'])
        newUser.set_password(info['password'])
        db.session.add(newUser)
        db.session.commit()
        flash('Account Created!')
        return redirect(url_for('loginPAge'))
    flash('invalid inptu')
    return redirect(url_for('signupPage'))

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("logged out")
    return redirect(url_for('index'))

@app.route('/userrecipes')
def showList():
    data = UserRecipe.query.all()
    print(data)
    return render_template('bookmark.html', data=data)

@app.route('/add/<n>')
@login_required
def addRecipe(n):
    reci = Recipe.query.get(n)
    check = UserRecipe.query.filter_by(userID=current_user.get_id(), recipeID=n).first()
    if check is None:
        userReci = UserRecipe(userID = current_user.get_id(), recipeID=reci.id, ingredients_list=reci.ingredients_list, name=reci.name)
        db.session.add(userReci)
        db.session.commit()
        flash("recipe added")
        return redirect(url_for('index'))
    else:
        flash("Recipe already in favourites")
        return redirect(url_for('index'))

@app.route('/remove/<n>')
@login_required
def removeRecipe(n):
    check = UserRecipe.query.get(n)
    db.session.delete(check)
    db.session.commit()
    return redirect(url_for('showList'))