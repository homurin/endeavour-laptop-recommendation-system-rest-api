import pandas as pd


def calculate_apps_system_requirements(apps=pd.DataFrame({})):
    min_cpu_speed = apps["minCpuSpeed"].max()
    min_cpu_cores = apps["minCores"].max()
    min_gpu_boost_clock = apps["minGpuBoostClock"].max()
    min_gpu_memory = apps["minGpuMemory"].max()
    min_direct_x = apps["minDirectX"].max()
    min_open_gl = apps["minOpenGl"].max()
    min_ram = apps["minRam"].max()
    min_storage = apps["minStorage"].sum()
    min_os = apps["buildNumber"].max()

    result = pd.DataFrame({
        "maxSpeed": [min_cpu_speed],
        "cores": [min_cpu_cores],
        "directX": [min_direct_x],
        "openGl": [min_open_gl],
        "gpuMemory": [min_gpu_memory],
        "gpuMaxSpeed": [min_gpu_boost_clock],
        "ram": [min_ram],
        "totalStorage": [min_storage],
        "buildNumber": [min_os],
    })

    return result
