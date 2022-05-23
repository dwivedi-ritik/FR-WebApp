from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
SECRET_KEY = 'f0d8251d0d29ebdd1c3032ebbafdde9b53d646f7d3677f09b760e7cada2126'
DB_URI = 'sqlite:///mydb.db'