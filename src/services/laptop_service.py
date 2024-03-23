import pandas as pd
import src.repository.app_repository as App
import src.repository.laptop_repository as Laptop
from src.utils.laptop_util import calculate_distance, calculate_similarity
from src.utils.application_util import calculate_apps_system_requirements


def recommendations_by_apps_req(app_ids: list = []):
    apps = App.find_by_ids(app_ids)
    laptops = Laptop.find_all()

    apps_req = calculate_apps_system_requirements(apps)

    imps_spec = laptops.drop(
        columns=["id", "name", "hddStorage", "ssdStorage"])

    distances = calculate_distance(imps_spec, apps_req)

    laptops["distances"] = distances[1:]

    recommendations = laptops.sort_values(
        by="distances", ascending=True).head(5)

    results = recommendations.to_dict(orient="records")

    return {"spec_req": apps_req.to_dict(orient="records"), "laptops": results}


def recommendations_by_spec(spec_req: dict):
    laptops = Laptop.find_all()

    imps_spec = laptops.drop(
        columns=["id", "name", "hddStorage", "ssdStorage"])

    spec_req = pd.DataFrame(
        [spec_req], columns=laptops.columns.to_list())

    ssd_req = spec_req["ssdStorage"]
    hdd_req = spec_req["hddStorage"]
    spec_req["storage"] = ssd_req + hdd_req

    imps_spec_req = spec_req[imps_spec.columns]

    distances = calculate_distance(imps_spec, imps_spec_req)

    laptops["distances"] = distances[1:]

    recommendations = laptops.sort_values(by="distances", ascending=True)
    top_recom = recommendations.head(5)
    results = top_recom.to_dict(orient="records")

    return results


def find_similar(id: str):
    laptops = Laptop.find_all()
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
