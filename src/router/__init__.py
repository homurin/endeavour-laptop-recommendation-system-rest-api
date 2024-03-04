from flask import Blueprint
from . import laptop
from . import cpu
main_blueprint = Blueprint("main", __name__, url_prefix="/")

main_blueprint.register_blueprint(laptop.laptop_blueprint)
main_blueprint.register_blueprint(cpu.cpu)
