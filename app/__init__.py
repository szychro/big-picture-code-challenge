from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .models import Book
    create_database(app)

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created database')
