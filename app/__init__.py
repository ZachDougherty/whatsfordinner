from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

from app import views
from app import models
