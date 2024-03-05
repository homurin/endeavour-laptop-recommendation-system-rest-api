import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class FlaskConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = os.environ.get("DEBUG")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO") or False
    SQLALCHEMY_TRACKMODIFICATION = os.getenv("SQLALCHEMY_TRACK_MODIFICATION")


class AppConfig:
    PORT = os.getenv("PORT")
    HOST = os.getenv("HOST")
