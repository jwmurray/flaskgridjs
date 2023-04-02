from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
    
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from app import routes, models
from app.models import User

def add_random_name():
    import names
    with app.app_context():
        name = User(name=names.get_last_name())
        db.session.add(name)
        db.session.commit() 