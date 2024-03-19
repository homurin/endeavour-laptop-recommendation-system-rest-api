import pandas as pd
from src.utils import laptop_util as Laptop, application_util as App
from src.utils.laptop_util import calculate_distance, calculate_similarity, filter_by_app_sysreq, filter_by_laptop_spec


def recommendations_by_apps_req(single_task_apps_id: list = [], multi_task_apps_id: list = []):
    single_task_apps = App.find_by_ids(single_task_apps_id)
    multi_task_apps = App.find_by_ids(multi_task_apps_id)

    apps_req = App.calculate_apps_system_requirements(
        single_task_apps, multi_task_apps)

    laptops = Laptop.clean_full_specs_dataframe()
    # filtered_laptops = filter_by_app_sysreq(laptops, apps_req)

    unused_cols = ["id", "name", "hddStorage", "ssdStorage"]

    imps_spec = laptops.drop(columns=unused_cols)
    # imps_spec_filtered = filtered_laptops.drop(columns=unused_cols)

    distances = calculate_distance(imps_spec, apps_req)
    # filtered_distances = calculate_distance(imps_spec_filtered, apps_req)

    laptops["distances"] = distances[1:]

    filtered_laptops = filter_by_app_sysreq(laptops, apps_req)

    recommendations = laptops.sort_values(
        by="distances", ascending=True).head(5)
    filtered_recom = filtered_laptops.sort_values(
        by="distances", ascending=True).head(5)

    results = recommendations.to_dict(orient="records")
    filtered_results = filtered_recom.to_dict(orient="records")

    spec_req = apps_req.to_dict(orient="records")

    return {"spec_req": spec_req, "laptops": results, "filteredSpec": filtered_results}


def recommendations_by_spec(spec_req: dict):
    laptops = Laptop.clean_full_specs_dataframe()

    unused_cols = ["id", "name", "totalStorage"]
    imps_spec = laptops.drop(columns=unused_cols)

    spec_req_df = pd.DataFrame(
        [spec_req], columns=imps_spec.columns.to_list())

    distances = calculate_distance(imps_spec, spec_req_df)

    laptops["distances"] = distances[1:]
    filtered_laptops = filter_by_laptop_spec(laptops, spec_req_df)

    recommendations = laptops.sort_values(by="distances", ascending=True)
    filtered_recom = filtered_laptops.sort_values(
        by="distances", ascending=True)

    top_recom = recommendations.head(5)
    filtered_laptops_recom = filtered_recom.head(5)

    results = top_recom.to_dict(orient="records")
    filtered_results = filtered_laptops_recom.to_dict(orient="records")

    return {"laptops": results, "filteredSpec": filtered_results}


def find_similar(id: str):
    laptops = Laptop.clean_full_specs_dataframe()

    laptop_params = laptops[laptops["id"] == id]

    if len(laptop_params) == 0:
        return dict([])

    imps_spec = laptops.drop(
        columns=["id", "name", "hddStorage", "ssdStorage"])
    target_index = laptop_params[imps_spec.columns].index[0]

    similarity = calculate_similarity(imps_spec, target_index)

    laptops["similarity"] = similarity
    recommendations = laptops.sort_values(by="similarity", ascending=False)
    condition = recommendations[recommendations["id"] == id].index
    recommendations.drop(condition, inplace=True)

    top_recom = recommendations.head(5)
    results = top_recom.to_dict(orient="records")
    return results
