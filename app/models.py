from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, SubmitField, PasswordField, \
					IntegerField
from wtforms.validators import DataRequired, Length

from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


# WTF Forms
class StringForm(FlaskForm):
	"Class for single string field form"
	field = StringField('url', validators=[DataRequired()])
	submit = SubmitField('submit')

class LoginForm(FlaskForm):
	"Login Form"
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	submit = SubmitField('submit')

class RegisterForm(FlaskForm):
	username = StringField('username', validators=[
		DataRequired(), Length(min=4, max=20)
	])
	password = PasswordField('password', validators=[
		DataRequired(), Length(min=8, max=20)
	])
	submit = SubmitField('submit')

class YesNoForm(FlaskForm):
	"Form for deciding to take an action or not"
	agree = SubmitField(label='Yes')
	disagree = SubmitField(label='No')

class RecipeForm(FlaskForm):
	title = StringField('title', validators=[DataRequired()])
	total_time = IntegerField('total_time', default=None)
	yields = StringField('yields', default=None)
	ingredients = StringField('ingredients', validators=[DataRequired()])
	instructions = StringField('instructions', validators=[DataRequired()])
	image = StringField('image', default=None)
	host = StringField('host', default=None)
	url = StringField('url', default='')  # need to decide if user recipes should be split from online
	submit = SubmitField('submit')

# Table <> Class definitions
class Recipes(db.Model):
	"Table for recipes"
	__tablename__ = "recipes"
	__table_args__ = {"schema": "public"}

	id = db.Column(db.Integer(), nullable=False, primary_key=True)
	created_at = db.Column(db.DateTime(), nullable=False)
	title = db.Column(db.String(), nullable=False)
	total_time = db.Column(db.Integer())
	yields = db.Column(db.String())
	ingredients = db.Column(db.ARRAY(db.String()), nullable=False)
	instructions = db.Column(db.ARRAY(db.String()), nullable=False)
	image = db.Column(db.String())
	host = db.Column(db.String())
	url = db.Column(db.String(), nullable=False)

	def to_dict(self):
		return {
			'id': self.id,
			'created_at': self.created_at,
			'title': self.title,
			'total_time': self.total_time,  # minutes
			'yields': self.yields,
			'ingredients': self.ingredients,  # list
			'instructions': self.instructions,  # list
			'image': self.image,  # url to image
			'host': self.host,  # host website
			'url': self.url  # original url
		}


class Users(db.Model, UserMixin):
	"Table for users"
	__tablename__ = "users"
	__table_args__ = {"schema": "public"}

	id = db.Column(db.Integer(), nullable=False, primary_key=True)
	username = db.Column(db.String(), nullable=False)
	password_hash = db.Column(db.String(), nullable=False)
	recipes = db.Column(db.ARRAY(db.Integer()))

	def __init__(self, username, password):
		self.username = username
		self.set_password(password)
		self.recipes = []

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id: int):
	return Users.query.get(int(id))
