import pandas as pd
from src.models import db, Laptop, Cpu, Gpu, Windows


def find_all():
    query = db.select(Laptop.id, Laptop.name,
                      Cpu.maxSpeed, Cpu.cores, Gpu.maxSpeed.label("gpuMaxSpeed"), Gpu.memory.label(
                          "gpuMemory"), Gpu.directX, Gpu.openGl,  Laptop.hddStorage,
                      Laptop.ssdStorage, Laptop.ram, Windows.buildNumber).join(Laptop.cpu).join(Laptop.gpu).join(Laptop.windows)

    df = pd.read_sql(query, con=db.engine)
    df["storage"] = df["ssdStorage"] + df["hddStorage"]
    return df
