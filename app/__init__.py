from flask import Flask
from flask_login import LoginManager, current_user, login_user, login_required
from .models import db
app = Flask(__name__)

login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.Database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = "SECRET"
    login_manager.init_app(app)
    db.init_app(app)
    return app

app = create_app()
app.app_context().push()
db.create_all(app=app)

from app import main