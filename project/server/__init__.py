# project/server/__init__.py


import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo
from flask_dropzone import Dropzone


# instantiate the extensions
login_manager = LoginManager()
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
mdb = PyMongo()
medb = MongoEngine()
dropzone = Dropzone()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static",
    )

    # set config
    app_settings = os.getenv("APP_SETTINGS", "project.server.config.DevelopmentConfig")
    app.config.from_object(app_settings)

    # set up extensions
    login_manager.init_app(app)
    bcrypt.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    dropzone.init_app(app)
    mdb.init_app(app)
    medb.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.server.user.views import user_blueprint
    from project.server.main.views import main_blueprint
    from project.server.stoltzmaniac.views import stoltzmaniac_blueprint
    from project.server.GregHilston.views import GregHilston_blueprint
    from project.server.twitter.views import twitter_blueprint
    from project.server.finance.views import finance_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(stoltzmaniac_blueprint)
    app.register_blueprint(GregHilston_blueprint)
    app.register_blueprint(twitter_blueprint)
    app.register_blueprint(finance_blueprint)

    # flask login
    from project.server.user.models import User

    login_manager.login_view = "user.login"
    login_manager.login_message_category = "danger"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    # error handlers
    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template("errors/401.html"), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/500.html"), 500

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
