from flask import Blueprint, request
import src.services.laptop_service as Laptop

laptop_blueprint = Blueprint(
    "laptop", __name__, url_prefix="/api/v1/")


@laptop_blueprint.route("/recommendations", methods=["POST"])
def laptop_recommendations_by_apps_req():
    try:
        request_body = request.get_json()
        app_ids = request_body["app_ids"]
        data = Laptop.recommendations_by_apps_req(app_ids)
        res = {"status": "success", "data": data}
        code = 200
        return (res, code)
    except:
        res = {"status": "failed", "message": "invalid request body", "requiredFields": [
            "app_ids: [list of app_id]"
        ]}
        code = 400
        return (res, 400)


@laptop_blueprint.route("/recommendations/<string:laptop_id>", methods=["GET"])
def similar_laptops(laptop_id):
    try:
        data = Laptop.find_similar(laptop_id)

        if (len(data) == 0):
            err_res = {"status": "failed",
                       "message": f"laptop with id {laptop_id} not found"}
            return (err_res, 404)

        res = {"status": "success", "laptops": data}
        code = 200
        return (res, code)
    except:
        res = {"status": "failed", "message": "invalid request fields",
               "requiredFields": "id"}
        code = 400
        return (res, code)
