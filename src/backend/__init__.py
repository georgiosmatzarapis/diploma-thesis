""" Main module for backend folder. """
from flask import Flask
from backend.helpers.logger import Logger
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_restplus import Api
from backend.helpers.main_config import CONFIGURATION


lg = Logger()
mongo = PyMongo()
bcrypt = Bcrypt()
api = Api(doc='/doc/', prefix='/api')


def create_app():
    """ Flask app utilization. """
    app = Flask(__name__, template_folder=f'../{CONFIGURATION.template_location}',
                static_folder=f'../{CONFIGURATION.static_location}')
    app.config['SECRET_KEY'] = CONFIGURATION.secret_key
    app.config['MONGO_URI'] = CONFIGURATION.mongo_uri
    app.config['PERMANENT_SESSION_LIFETIME'] = CONFIGURATION.permanent_session_lifetime

    # Initialize flask app with extentions
    mongo.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app)

    # Blueprints - web app
    from backend.web.web_app.users_auth.routes import users
    from backend.web.web_app.main.routes import main
    from backend.web.web_app.errors.handlers import errors
    from backend.web.web_app.allergy_settings.routes import allergy_settings

    # Namespaces - web api
    from backend.web.web_api.home.routes import NAMESPACE as home_ns
    from backend.web.web_api.myhealth.routes import NAMESPACE as myhealth_ns

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(allergy_settings)

    api.add_namespace(home_ns)
    api.add_namespace(myhealth_ns)

    return app
