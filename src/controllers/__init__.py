from flask import Blueprint
from . import laptop_controller

main_blueprint = Blueprint("main", __name__, url_prefix="/")


main_blueprint.register_blueprint(laptop_controller.laptop_blueprint)
