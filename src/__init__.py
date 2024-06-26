from flask import Flask
from flask_cors import CORS
from config import AppConfig, FlaskConfig
from src.controllers import main_blueprint
from src.models import db


def create_app(config_class=FlaskConfig):
    app = Flask(__name__)
    CORS(app)
    app.json.sort_keys = False
    app.config.from_object(config_class)
    app.register_blueprint(main_blueprint)
    db.init_app(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=AppConfig.HOST, port=AppConfig.PORT)
