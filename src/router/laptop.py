from flask import Blueprint
from src.controllers.laptop import LaptopController

laptop_blueprint = Blueprint(
    "laptop", __name__, url_prefix="/api/v1/laptops")


@laptop_blueprint.get("/")
def test():
    return LaptopController.test()


# @laptop.get("/system_recommendation")
# def get_all():
#     return LaptopController.get_all()
