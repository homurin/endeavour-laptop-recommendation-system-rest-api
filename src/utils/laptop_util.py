import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from scipy.stats import zscore
from src.models import db, Laptop, Cpu, Gpu, Windows


def clean_full_specs_dataframe():
    query = db.select(Laptop.id, Laptop.name, Laptop.hddStorage,
                      Laptop.ssdStorage, Laptop.ram, Cpu.baseSpeed,
                      Cpu.cores, Gpu.maxSpeed.label("gpuMaxSpeed"), Gpu.memory.label("gpuMemory"), Gpu.directX, Gpu.openGl, Windows.buildNumber).join(Laptop.cpu).join(Laptop.gpu).join(Laptop.windows)

    df = pd.read_sql(query, con=db.engine)
    df["totalStorage"] = df["ssdStorage"] + df["hddStorage"]
    return df


def calculate_distance(laptops: pd.DataFrame, sys_req: pd.DataFrame):

    merged_df = pd.concat(
        [sys_req, laptops], ignore_index=True)
    normalized = merged_df.apply(zscore)
    norm_spec_req = normalized.values[0].reshape(1, -1)

    distance = euclidean_distances(
        normalized, norm_spec_req)

    return distance


def calculate_similarity(laptops: pd.DataFrame, index: pd.DataFrame):
    normalized = laptops.apply(zscore)
    norm_target = normalized.values[index].reshape(1, -1)

    similarity = cosine_similarity(normalized, norm_target)

    return similarity


def filter_by_app_sysreq(laptops: pd.DataFrame, target: pd.DataFrame):
    baseSpeed = (laptops["baseSpeed"] >= target["baseSpeed"].values[0])
    cores = (laptops["cores"] >= target["cores"].values[0])
    gpuMaxSpeed = (laptops["gpuMaxSpeed"] >= target["gpuMaxSpeed"].values[0])
    directX = (laptops["directX"] >= target["directX"].values[0])
    openGl = (laptops["openGl"] >= target["openGl"].values[0])
    totalStorage = (laptops["totalStorage"] >
                    target["totalStorage"].values[0])
    vramFromRam = target["gpuMemory"].values[0] - laptops["gpuMemory"]
    laptops["vramFromRam"] = vramFromRam
    laptops.loc[laptops["vramFromRam"] <= 0, "vramFromRam"] = 0
    ram = (laptops["ram"] >= (
        target["ram"].values[0] + laptops["vramFromRam"]))
    buildNumber = (laptops["buildNumber"] >= target["buildNumber"].values[0])

    laptops = laptops.loc[baseSpeed &
                          cores & gpuMaxSpeed & directX & openGl & ram & totalStorage & buildNumber]

    return laptops


def filter_by_laptop_spec(laptops: pd.DataFrame, target: pd.DataFrame):
    baseSpeed = (laptops["baseSpeed"] >= target["baseSpeed"].values[0])
    cores = (laptops["cores"] >= target["cores"].values[0])
    directX = (laptops["directX"] > target["directX"].values[0])
    openGl = (laptops["openGl"] >= target["openGl"].values[0])
    gpuMaxSpeed = (laptops["gpuMaxSpeed"] >= target["gpuMaxSpeed"].values[0])
    hddStorage = (laptops["ssdStorage"] >=
                  target["ssdStorage"].values[0])
    ssdStorage = (laptops["hddStorage"] >=
                  target["hddStorage"].values[0])
    vramFromRam = target["gpuMemory"].values[0] - laptops["gpuMemory"]
    laptops["vramFromRam"] = vramFromRam
    laptops.loc[laptops["vramFromRam"] <= 0, "vramFromRam"] = 0
    ram = (laptops["ram"] >= (
        target["ram"].values[0] + laptops["vramFromRam"]))
    buildNumber = (laptops["buildNumber"] >= target["buildNumber"].values[0])
    laptops = laptops.loc[baseSpeed &
                          cores & gpuMaxSpeed & ram & directX & openGl & ssdStorage & hddStorage & buildNumber]

    return laptops
