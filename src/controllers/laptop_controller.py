from flask import Blueprint, request
from src.services.laptop_service import recommendations_by_apps_req

laptop_blueprint = Blueprint(
    "laptop", __name__, url_prefix="/api/v1/laptops")


@laptop_blueprint.route("/recommendations-by-apps-req", methods=["POST"])
def laptop_recommendations_by_apps_req():
    try:
        app_req = request.get_json()
        single_task_apps_id = app_req["single_task_apps_id"]
        multi_task_apps_id = app_req["multi_task_apps_id"]
        data = recommendations_by_apps_req(
            single_task_apps_id, multi_task_apps_id)

        return ({"status": "success", "data": data}, 200)
    except:
        return ({"status": "failed", "message": "invalid request body", "requiredBody": [
            {"single_task_apps_id": ["app_id"],
             "multi_task_apps_id": ["app_id"]}
        ]}, 400)
