import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from scipy.stats import zscore


def calculate_distance(laptops: pd.DataFrame, system_requirements: pd.DataFrame):
    merged_data = pd.concat(
        [system_requirements, laptops], ignore_index=True)
    normalized = merged_data.apply(zscore)

    norm_spec_req = normalized.values[0].reshape(1, -1)

    distance = euclidean_distances(
        normalized, norm_spec_req)

    return distance


def calculate_similarity(laptops: pd.DataFrame, index: pd.DataFrame):
    normalized = laptops.apply(zscore)
    norm_target = normalized.values[index].reshape(1, -1)

    similarity = cosine_similarity(normalized, norm_target)

    return similarity


def filter_irelevant(laptops: pd.DataFrame, sys_req: pd.DataFrame) -> pd.DataFrame:
    cpuSpeed = (laptops["cpuMaxSpeed"] >= sys_req["cpuMaxSpeed"].values[0])
    cores = (laptops["cores"] >= sys_req["cores"].values[0])
    gpuMaxSpeed = (laptops["gpuMaxSpeed"] >=
                   sys_req["gpuMaxSpeed"].values[0])
    directX = (laptops["directX"] >= sys_req["directX"].values[0])
    openGl = (laptops["openGl"] >= sys_req["openGl"].values[0])
    totalStorage = (laptops["totalStorage"] >=
                    sys_req["totalStorage"].values[0])
    buildNumber = (laptops["buildNumber"] >=
                   sys_req["buildNumber"].values[0])
    vramFromRam = sys_req["gpuMemory"].values[0] - laptops["gpuMemory"]
    laptops["vramFromRam"] = vramFromRam

    laptops.loc[laptops["vramFromRam"] <= 0, "vramFromRam"] = 0

    ram = (laptops["ram"] >= (
        sys_req["ram"].values[0] + laptops["vramFromRam"]))

    filtered = laptops.loc[cpuSpeed & cores & gpuMaxSpeed &
                           directX & openGl & ram & totalStorage & buildNumber]
    filtered = filtered.drop(columns=["hddStorage", "ssdStorage"])

    return filtered
