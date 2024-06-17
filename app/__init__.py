import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'

    from app.routes import main as main_blueprint
    from app.auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app

from app import models
