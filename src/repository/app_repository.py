import pandas as pd
from src.models import db, Application as App, Windows as Wind


def find_by_ids(apps_id: list = [""]):
    query = db.select(App.id, App.minCpuSpeed, App.minCores, App.minDirectX, App.minOpenGl,
                      App.minGpuBoostClock, App.minGpuMemory, App.minRam, App.minStorage, Wind.buildNumber).join(App.windows).where(App.id.in_(apps_id))

    dataframe = pd.read_sql(query, con=db.engine)

    if dataframe.empty:
        no_data = pd.DataFrame({
            "id": ["0"],
            "minCpuSpeed": [0],
            "minCores": [0],
            "minDirectX": [0],
            "minOpenGl": [0],
            "minGpuMemory": [0],
            "minGpuBoostClock": [0],
            "minRam": [0],
            "minStorage": [0],
            "buildNumber": [0],
        })
        return no_data
    return dataframe
