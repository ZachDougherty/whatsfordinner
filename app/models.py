from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from app import db

class StringForm(FlaskForm):
	"Class for single string field form"
	field = StringField('url', validators=[DataRequired()])
	submit = SubmitField('submit')

class Recipes(db.Model):
	"Table for recipes"
	__tablename__ = "recipes"
	__table_args__ = {"schema": "public"}

	id = db.Column(db.Integer(), nullable=False, primary_key=True)
	title = db.Column(db.String(), nullable=False)
	total_time = db.Column(db.Integer())
	yields = db.Column(db.String())
	ingredients = db.Column(db.ARRAY(db.String()), nullable=False)
	instructions = db.Column(db.ARRAY(db.String()), nullable=False)
	image = db.Column(db.String())
	host = db.Column(db.String())
	url = db.Column(db.String(), nullable=False)
	
