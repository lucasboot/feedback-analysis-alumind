from flask import Flask
from flask_cors import CORS
from app.config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app)

    from .routes.feedback_routes import feedback_routes
    from .routes.pages_routes import pages_routes
    app.register_blueprint(feedback_routes)
    app.register_blueprint(pages_routes)

    return app
