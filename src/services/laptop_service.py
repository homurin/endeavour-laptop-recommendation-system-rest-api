import pandas as pd
from src.utils import laptop_util as Laptop, application_util as App
from src.utils.laptop_util import calculate_distance, calculate_similarity


def recommendations_by_apps_req(single_task_apps_id: list = [], multi_task_apps_id: list = []):
    single_task_apps = App.find_by_ids(single_task_apps_id)
    multi_task_apps = App.find_by_ids(multi_task_apps_id)

    apps_req = App.calculate_apps_system_requirements(
        single_task_apps, multi_task_apps)

    laptops = Laptop.clean_full_specs_dataframe()

    ssd = laptops["ssdStorage"]
    hdd = laptops["hddStorage"]
    laptops["storage"] = ssd + hdd

    imps_spec = laptops.drop(
        columns=["id", "name", "hddStorage", "ssdStorage"])

    distances = calculate_distance(imps_spec, apps_req)

    laptops["distances"] = distances[1:]

    recommendations = laptops.sort_values(
        by="distances", ascending=True).head(5)

    results = recommendations.to_dict(orient="records")

    return {"spec_req": apps_req.to_dict(orient="records"), "laptops": results}


def recommendations_by_spec(spec_req: dict):
    laptops = Laptop.clean_full_specs_dataframe()

    ssd = laptops["ssdStorage"]
    hdd = laptops["hddStorage"]
    laptops["storage"] = ssd + hdd

    imps_spec = laptops.drop(
        columns=["id", "name", "hddStorage", "ssdStorage"])

    spec_req_df = pd.DataFrame(
        [spec_req], columns=laptops.columns.to_list())
    ssd_req = spec_req_df["ssdStorage"]
    hdd_req = spec_req_df["hddStorage"]
    spec_req_df["storage"] = ssd_req + hdd_req
    spec_req_df = spec_req_df[imps_spec.columns]

    distances = calculate_distance(imps_spec, spec_req_df)

    laptops["distances"] = distances[1:]

    recommendations = laptops.sort_values(by="distances", ascending=True)
    top_recom = recommendations.head(5)
    results = top_recom.to_dict(orient="records")

    return results


def find_similar(id: str):
    laptops = Laptop.clean_full_specs_dataframe()
    ssd = laptops["ssdStorage"]
    hdd = laptops["hddStorage"]
    laptops["storage"] = ssd + hdd
    laptop_target = laptops[laptops["id"] == id]

    if len(laptop_target) == 0:
        return dict([])

    imps_spec = laptops.drop(
        columns=["id", "name", "hddStorage", "ssdStorage"])
    target_index = laptop_target[imps_spec.columns].index[0]

    similarity = calculate_similarity(imps_spec, target_index)

    laptops["similarity"] = similarity

    recommendations = laptops.sort_values(by="similarity", ascending=False)
    top_recom = recommendations.head(6)
    results = top_recom.to_dict(orient="records")[1:]
    return results
