from flask import Flask
from config import AppConfig, FlaskConfig
from src.controllers import main_blueprint
from src.models import db


def create_app(config_class=FlaskConfig):
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config.from_object(config_class)
    app.register_blueprint(main_blueprint)
    db.init_app(app)
    return app


app = create_app()


if __name__ == "main":
    app.run(host=AppConfig.HOST, port=AppConfig.HOST)
