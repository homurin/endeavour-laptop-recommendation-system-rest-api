import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from scipy.stats import zscore


def calculate_distance(laptops: pd.DataFrame, system_requirements: pd.DataFrame):
    merged_df = pd.concat(
        [system_requirements, laptops], ignore_index=True)
    normalized = merged_df.apply(zscore)
    norm_spec_req = normalized.values[0].reshape(1, -1)
    print(normalized)
    distance = euclidean_distances(
        normalized, norm_spec_req)

    return distance


def calculate_similarity(laptops: pd.DataFrame, index: pd.DataFrame):
    normalized = laptops.apply(zscore)
    norm_target = normalized.values[index].reshape(1, -1)

    similarity = cosine_similarity(normalized, norm_target)

    return similarity


def filter_irelevant(laptops: pd.DataFrame):
    pass
