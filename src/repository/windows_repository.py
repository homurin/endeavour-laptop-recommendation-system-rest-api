import pandas as pd
from src.models import db, Windows


def find_windows_by_build_number(build_number: int):
    query = db.select(Windows.id, Windows.name, Windows.buildNumber).where(
        Windows.buildNumber == build_number)

    df = pd.read_sql(query, con=db.engine)

    return df
