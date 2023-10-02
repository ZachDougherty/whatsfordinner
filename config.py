import os

class Config():
	SECRET_KEY = os.urandom(24)
	SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/whatsfordinner"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
