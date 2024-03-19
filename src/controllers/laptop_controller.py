from flask import Blueprint, request
import src.services.laptop_service as Laptop
from src.utils.laptop_util import clean_full_specs_dataframe

laptop_blueprint = Blueprint(
    "laptop", __name__, url_prefix="/api/v1/laptops")


@laptop_blueprint.route("/recommendations-by-apps-req", methods=["POST"])
def laptop_recommendations_by_apps_req():
    try:
        app_req = request.get_json()
        single_task_apps_id = app_req["single_task_apps_id"]
        multi_task_apps_id = app_req["multi_task_apps_id"]

        data = Laptop.recommendations_by_apps_req(
            single_task_apps_id, multi_task_apps_id)
        res = {"status": "success", "data": data}
        code = 200
        return (res, code)
    except ValueError:
        res = {"status": "failed", "message": "invalid request body", "errorType": "ValueError", "requiredFields": [
            {"single_task_apps_id": ["list of app_id"],
             "multi_task_apps_id": ["list of app_id"]}
        ]}
        code = 400
        return (res, 400)


@laptop_blueprint.route("/recommendations-by-specs", methods=["POST"])
def laptop_recommendations_by_req():
    try:
        spec_req = request.get_json()
        data = Laptop.recommendations_by_spec(spec_req)
        res = {"status": "success", "data": data}
        code = 200
        return (res, code)
    except ValueError:
        columns = clean_full_specs_dataframe().columns.to_list()[2:]
        columns.pop()

        res = {"status": "failed", "message": "invalid request fields", "errorType": "ValueError",
               "requiredFields": columns}
        code = 400
        return (res, code)


@laptop_blueprint.route("/similar-laptops", methods=["POST"])
def similar_laptops():
    try:
        req = request.get_json()
        id = req["id"].replace(" ", "")
        data = Laptop.find_similar(id)

        if id == "":
            raise ValueError({"status": "failed", "message": "invalid request fields", "errorType": "ValueError",
                              "requiredFields": "id"})
        if (len(data) == 0):
            err_res = {"status": "failed",
                       "message": f"laptop with id {id} not found"}
            return (err_res, 404)
        res = {"status": "success", "laptops": data}
        code = 200
        return (res, code)
    except ValueError:
        res = {"status": "failed", "message": "invalid request fields", "errorType": "ValueError",
               "requiredFields": "id"}
        code = 400
        return (res, code)
