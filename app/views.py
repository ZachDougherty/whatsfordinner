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
	url = request.args.get('url')
	try:
		recipe = models.Recipes.query.filter_by(url=url).first()
		recipe_dict = get_recipe(url)
		if not recipe:
			recipe = models.Recipes(**recipe_dict)
			db.session.add(recipe)
			db.session.commit()
	except:  # if website is not implemented by recipe_scrapers or url is bad
		recipe_dict = None
	finally:
		return render_template('recipe.html', recipe=recipe_dict)
