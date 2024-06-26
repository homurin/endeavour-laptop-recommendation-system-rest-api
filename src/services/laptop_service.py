import pandas as pd
import src.repository.app_repository as App
import src.repository.laptop_repository as Laptop
from src.utils.laptop_util import calculate_distance, calculate_similarity, filter_irrelevant
from src.utils.application_util import calculate_apps_system_requirements
from src.repository.windows_repository import find_windows_by_build_number

dropedColumn = ["id", "name", "thumb", "cpuName", "cpuBaseSpeed",
                "gpuName", "gpuBaseSpeed", "hddStorage", "ssdStorage", "windowsName", "osEdition"]


def recommendations_by_apps_req(app_ids: list = []):
    apps = App.find_by_ids(app_ids)
    laptops = Laptop.find_all()

    apps_req = calculate_apps_system_requirements(apps)

    imps_spec = laptops.drop(columns=dropedColumn)

    distances = calculate_distance(imps_spec, apps_req)

    laptops["distances"] = distances[1:]

    filtered = filter_irrelevant(laptops, apps_req)

    sorted = filtered.sort_values(by="distances", ascending=True)
    top_laptops = sorted.head(5)
    results = top_laptops.to_dict(orient="records")
    mapped = mapped_results(results)

    app_req_dict = apps_req.to_dict(orient="records")[0]
    windows = find_windows_by_build_number(
        app_req_dict["buildNumber"]).to_dict(orient="records")[0]

    windowsName = windows["name"]
    app_req_dict["windowsName"] = windowsName

    return {"spec_req": app_req_dict, "laptops": mapped}


def find_similar(id: str):
    laptops = Laptop.find_all()
    laptop_target = laptops[laptops["id"] == id]

    if len(laptop_target) == 0:
        return dict([])

    imps_spec = laptops.drop(columns=dropedColumn)

    target_index = laptop_target[imps_spec.columns].index[0]

    similarity = calculate_similarity(imps_spec, target_index)

    laptops["similarity"] = similarity

    sorted = laptops.sort_values(by="similarity", ascending=False)
    filtered = sorted[sorted['similarity'] > 0].head(6)
    results = filtered[filtered["id"] != id] .to_dict(orient="records")
    mapped = mapped_results(results)
    return mapped


def mapped_results(list: list):
    mapped = []
    for laptop in list:
        obj = {
            "id": laptop["id"],
            "name": laptop["name"],
            "thumb": laptop["thumb"],
            "ram": laptop["ram"],
            "ssdStorage": laptop["ssdStorage"],
            "hddStorage": laptop["hddStorage"],
            "totalStorage": laptop["totalStorage"],
            "osEdition": laptop["osEdition"],
            "cpu": {
                "name": laptop["cpuName"],
                "baseSpeed": laptop["cpuBaseSpeed"],
                "maxSpeed": laptop["cpuMaxSpeed"],
                "cores": laptop["cpuCores"]},
            "gpu": {
                "name": laptop["gpuName"],
                "baseSpeed": laptop["gpuBaseSpeed"],
                "maxSpeed": laptop["gpuMaxSpeed"],
                "memory": laptop["gpuMemory"],
                "directX": laptop["directX"],
                "openGl": laptop["openGl"],
            },
            "windowsVersion": {
                "name": laptop["windowsName"],
                "buildNumber": laptop["buildNumber"]
            }
        }

        mapped.append(obj)
    return mapped
