import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv

from app.utils.middlewares import UnexceptedErrorsMiddleware


load_dotenv()


app = Flask(__name__)
api = Api(app)

app.wsgi_app = UnexceptedErrorsMiddleware(app.wsgi_app)

env_config = os.getenv("APP_SETTINGS", "app.config.DevelopmentConfig")
app.config.from_object(env_config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import manage

from app import auth
from app import resources

