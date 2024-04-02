import pandas as pd
from src.models import db, Laptop, Cpu, Gpu, Windows


def find_all():
    query = db.select(Laptop.id, Laptop.name, Laptop.thumb, Cpu.name.label("cpuName"), Cpu.baseSpeed.label("cpuBaseSpeed"), Cpu.maxSpeed.label("cpuMaxSpeed"), Cpu.cores.label("cpuCores"), Gpu.name.label("gpuName"), Gpu.baseSpeed.label("gpuBaseSpeed"), Gpu.maxSpeed.label("gpuMaxSpeed"), Gpu.memory.label("gpuMemory"), Gpu.directX, Gpu.openGl, Laptop.hddStorage,
                      Laptop.ssdStorage, Laptop.ram, Windows.name.label("windowsName"), Laptop.osEdition, Windows.buildNumber).join(Laptop.cpu).join(Laptop.gpu).join(Laptop.windows)

    df = pd.read_sql(query, con=db.engine)
    df["totalStorage"] = df["ssdStorage"] + df["hddStorage"]
    return df
