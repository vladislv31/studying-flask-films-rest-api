import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
api = Api(app)

env_config = os.getenv("APP_SETTINGS", "app.config.DevelopmentConfig")
app.config.from_object(env_config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import resources
from app import models

