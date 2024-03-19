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


def calculate_apps_system_requirements(single_task_apps=pd.DataFrame({}), multi_task_apps=pd.DataFrame({})):
    min_cpu_base_speed = max([single_task_apps["minCpuSpeed"].max(),
                              multi_task_apps["minCpuSpeed"].max()])
    min_cpu_cores = max([single_task_apps["minCores"].max(),
                        multi_task_apps["minCores"].max()])
    min_direct_ver = max(
        [single_task_apps["minDirectX"].max(), multi_task_apps["minDirectX"].max()])
    min_open_gl = max(
        [single_task_apps["minOpenGl"].max(), multi_task_apps["minOpenGl"].max()])
    min_gpu_memory = max(
        [single_task_apps["minGpuMemory"].max(), multi_task_apps["minGpuMemory"].sum()])
    min_gpu_boost_clock = max(
        [single_task_apps["minGpuBoostClock"].max(), multi_task_apps["minGpuBoostClock"].max()])
    min_ram = max(
        [single_task_apps["minRam"].max(), multi_task_apps["minRam"].sum()])
    min_storage = sum(
        [single_task_apps["minStorage"].sum(), multi_task_apps["minStorage"].sum()])
    min_os = sum(
        [single_task_apps["buildNumber"].max(), multi_task_apps["buildNumber"].max()])

    result = pd.DataFrame({
        "baseSpeed": [min_cpu_base_speed],
        "cores": [min_cpu_cores],
        "directX": [min_direct_ver],
        "openGl": [min_open_gl],
        "gpuMemory": [min_gpu_memory / 1000],
        "gpuMaxSpeed": [min_gpu_boost_clock],
        "ram": [min_ram],
        "totalStorage": [min_storage],
        "buildNumber": [min_os],
    })

    return result
