from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this is my secret key'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/recipe'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Recipe

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all(app=app)
        print('Created Database!')
        
        #load default data
        from .models import User, Recipe
        from werkzeug.security import generate_password_hash

        app.app_context().push()
        user = User.query.filter_by(email='randall-chan@rocketmail.com').first()
        try:
            user
        except:
            newuser = User(first_name='Randall Chan', email='randall-chan@rocketmail.com', password=generate_password_hash('password', method='sha256'))
            print(newuser)
            db.session.add(newuser)
            db.session.commit()