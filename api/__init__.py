from flask import Flask
from flask_restx import Api
from dotenv import load_dotenv
import os
from .utils import db
from datetime import timedelta
from flask_jwt_extended import JWTManager
from .auth.user import user_namespace
from .tools.devlink import link_namespace
from flask_migrate import Migrate
from flask_cors import CORS
load_dotenv()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'eff90282dhdgtw'
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=60)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    JWTManager(app)
    Migrate(app, db)

    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        },
    }

    api = Api(app, security= 'apikey', title='DevLink BackEnd', version='1.0', authorizations = authorizations)

    api.authorizations = authorizations

    api.add_namespace(user_namespace, path='/api/auth')
    api.add_namespace(link_namespace, path='/api/link')
    CORS(app, origin=api)

    return app