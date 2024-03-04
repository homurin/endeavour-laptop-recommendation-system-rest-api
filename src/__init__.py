from flask import Flask
from dotenv import load_dotenv
from config import AppConfig, FlaskConfig
from src.router import main_blueprint

load_dotenv()


def create_app(config_class=FlaskConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(main_blueprint)
    return app


app = create_app()

if __name__ == "main":
    app.run(host=AppConfig.HOST, port=AppConfig.HOST)
