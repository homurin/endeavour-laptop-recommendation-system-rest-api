from flask import Blueprint

cpu = Blueprint("cpu", __name__, url_prefix="/api/v1/cpu")


@cpu.get("/")
def test():
    return {"data": []}
