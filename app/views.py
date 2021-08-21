from flask import redirect, url_for, render_template, request

from app import app, db, models
from app.models import StringForm
from app.scrape import get_recipe

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
	"""
	Need to improve the flow of this function.
	Trying to catch errors by type checking the
	output of a function is clunky and
	confusing, I need to refactor this.
	"""
	url = request.args.get('url')
	response = get_recipe(url)
	if isinstance(response, str):
		recipe_dict = None
	else:
		recipe_dict = response
	recipe = models.Recipes.query.filter_by(url=url).first()
	if recipe_dict is not None and not recipe:
		recipe = models.Recipes(**recipe_dict)
		db.session.add(recipe)
		db.session.commit()
	return render_template('recipe.html', recipe=recipe_dict)


@app.route('/testing')
def testing():
	"Test route for checking db connection"
	rows = models.GODT.query.filter_by(year=2012)
	return render_template('test.html', rows=rows)
