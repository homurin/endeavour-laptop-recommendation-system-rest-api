import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from scipy.stats import zscore
from src.utils import laptop_util as Laptop, application_util as App


def recommendations_by_apps_req(single_task_apps_id: list = [], multi_task_apps_id: list = []):
    single_task_apps = App.find_by_ids(single_task_apps_id)
    multi_task_apps = App.find_by_ids(multi_task_apps_id)

    apps_req = App.calculate_apps_system_requirements(
        single_task_apps, multi_task_apps)

    laptops_spec = Laptop.clean_full_specs_dataframe()

    laptops_spec["storage"] = laptops_spec["ssdStorage"] + \
        laptops_spec["hddStorage"]

    imps_spec = laptops_spec.drop(
        columns=["id", "name", "hddStorage", "ssdStorage"])

    distance = calculate_distance(imps_spec, apps_req)

    laptops_spec["distance"] = distance[1:]

    recommendation = laptops_spec.sort_values(
        by="distance", ascending=True).head(5)

    results = recommendation.to_dict(orient="records")

    return {"spec_req": apps_req.to_dict(orient="records"), "recommendations": results}


def calculate_distance(laptops_spec: pd.DataFrame, system_requirements: pd.DataFrame):
    merged_data = pd.concat(
        [system_requirements, laptops_spec], ignore_index=True)
    normalized = merged_data.apply(zscore)
    norm_spec_req = normalized.values[0].reshape(1, -1)

    distance = euclidean_distances(
        normalized, norm_spec_req)

    return distance
