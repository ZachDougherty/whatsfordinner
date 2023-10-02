from datetime import datetime
from flask import redirect, url_for, render_template, request, flash
from flask_login.utils import login_user, logout_user, \
							  current_user, login_required
from recipe_scrapers import WebsiteNotImplementedError

from app import app, db, models
from app.models import StringForm, LoginForm, RegisterForm, Users, \
					   Recipes, RecipeForm
from app.scrape import get_recipe

import json

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
	"Home page for Whatsfordinner"
	form = StringForm()
	if form.validate_on_submit():
		url = str(form.field.data)
		return redirect(url_for('recipe', url=url))
	return render_template('index.html', form=form)

@app.route('/cookbook', methods=['GET','POST','PUT'])
@login_required
def cookbook():
	"Contains all user recipes"
	form = StringForm()
	if form.validate_on_submit():
		url = form.field.data
		recipe = models.Recipes.query.filter_by(url=url).first()
		if not recipe:
			try:
				recipe_dict = get_recipe(url)
				recipe_dict["created_at"] = datetime.utcnow()
				recipe = models.Recipes(**recipe_dict)
				db.session.add(recipe)
			# TODO: better error handling
			except Exception as e:  # if website is not implemented by recipe_scrapers or url is bad
				flash("Sorry, this website has not been implemented yet.")
		if recipe.id not in current_user.recipes:
			current_user.recipes = current_user.recipes + [recipe.id]
	db.session.commit()

	recipes = sorted([
		Recipes.query.get(id).to_dict() for id in current_user.recipes if id is not None
	], key=lambda x: x["created_at"], reverse=True)
	return render_template('cookbook.html', form=form, recipes=recipes)

@app.route('/recipe/<id>', methods=['POST','GET'])
def recipe_user(id: int):
	"Display user's recipe information."
	recipe = models.Recipes.query.get(id).to_dict()

	return render_template('recipe.html', recipe=recipe)

@app.route('/recipe', methods=['POST','GET'])
def recipe():
	"Display recipe information."
	url = request.args.get('url')
	try:
		recipe_dict = get_recipe(url)
	except:
		recipe_dict = None
	return render_template('recipe.html', recipe=recipe_dict)

@app.route('/login', methods=['GET','POST'])
def login():
	"Login page"
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
	"Register page"
	form = RegisterForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = Users.query.filter_by(username=username).first()
		if not user:
			# allow user to preselect recipes from the catalog
			new_user = Users(username, password)
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user)
			return render_template('index.html', form=StringForm(),
				loggedin=current_user.is_authenticated)
		flash("User already exists. ")

	return render_template('register.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	"Logout page"
	logout_user()
	return render_template('index.html', form=StringForm(),
		loggedin=current_user.is_authenticated)


@app.route('/test', methods=['GET','POST'])
def see_user():
	form = RecipeForm()
	data = ''
	if form.validate_on_submit():
		data = form.data

	return render_template('test.html', form=form, data=data)
