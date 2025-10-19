from flask import Flask
from .extensions import ma
from .models import db
from .blueprints.members import members_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    #initialize extensions
    ma.init_app(app)
    db.init_app(app) 

    #Register Blueprints
    app.register_blueprint(members_bp, url_prefix='/members')

    return app