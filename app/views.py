from flask import redirect, url_for, render_template, request, flash
from flask_login.utils import login_user, logout_user, \
							  current_user, login_required

from app import app, db, models
from app.models import StringForm, LoginForm, RegisterForm, Users
from app.scrape import get_recipe

import json

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
	form = StringForm()
	if form.validate_on_submit():
		url = str(form.field.data)
		return redirect(url_for('recipe', url=url))
	return render_template('index.html', form=form)

@app.route('/recipe', methods=['POST','GET'])
def recipe():
	"Display recipe information."
	url = request.args.get('url')
	try:
		recipe = models.Recipes.query.filter_by(url=url).first()
		recipe_dict = get_recipe(url)
		with open(f"{recipe_dict['title']}.json", "w") as out:
			json.dump(recipe_dict, out)
		if not recipe:
			recipe = models.Recipes(**recipe_dict)
			db.session.add(recipe)
			db.session.commit()
			with open(f"recipes/{recipe_dict['title']}.json", "w") as out:
				json.dump(recipe_dict, out)
	except:  # if website is not implemented by recipe_scrapers or url is bad
		recipe_dict = None
	finally:
		return render_template('recipe.html', recipe=recipe_dict)

@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = Users.query.filter_by(username=username).first()
		if not user:
			flash(f"Username: {username} not found")
		elif not user.check_password(password):
			flash("Incorrect password")
		else:
			login_user(user)
			return render_template('index.html', form=StringForm(),
				loggedin=current_user.is_authenticated)

	return render_template('login.html', form=form,
						   loggedin=current_user.is_authenticated)

@app.route('/register', methods=['GET','POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = Users.query.filter_by(username=username).first()
		if not user:
			new_user = Users(username, password)
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user)
			return render_template('index.html', form=StringForm(),
				loggedin=current_user.is_authenticated)
		flash("Incorrect")

	return render_template('register.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('index.html', form=StringForm(),
		loggedin=current_user.is_authenticated)
