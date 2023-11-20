from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "iush_database"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Mohanad_Dreamer'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:Mysql_201@localhost/{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from . import models
    
    with app.app_context():
        db.create_all()
        print("Database is successfully created! ")
    
    return app
