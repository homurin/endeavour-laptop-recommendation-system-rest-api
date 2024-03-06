import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from scipy.stats import zscore
from src.models import db, Laptop, Cpu, Gpu, Windows


def clean_full_specs_dataframe():
    query = db.select(Laptop.id, Laptop.name, Laptop.hddStorage,
                      Laptop.ssdStorage, Laptop.ram, Cpu.baseSpeed,
                      Cpu.maxSpeed, Cpu.cores, Cpu.threads, Gpu.maxSpeed.label("gpuMaxSpeed"), Gpu.memory.label("gpuMemory"), Gpu.directX, Gpu.openGl, Windows.buildNumber).join(Laptop.cpu).join(Laptop.gpu).join(Laptop.windows)

    df = pd.read_sql(query, con=db.engine)
    df["storage"] = df["ssdStorage"] + df["hddStorage"]
    return df


def calculate_distance(laptops: pd.DataFrame, system_requirements: pd.DataFrame):
    merged_df = pd.concat(
        [system_requirements, laptops], ignore_index=True)
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
