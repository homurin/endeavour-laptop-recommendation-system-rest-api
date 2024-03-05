import pandas as pd
from src.models import db, Laptop, Cpu, Gpu, Windows


def clean_full_specs_dataframe():
    query = db.select(Laptop.id, Laptop.name, Laptop.hddStorage,
                      Laptop.ssdStorage, Laptop.ram, Cpu.baseSpeed,
                      Cpu.maxSpeed, Cpu.cores, Cpu.threads, Gpu.maxSpeed.label("gpuMaxSpeed"), Gpu.memory.label("gpuMemory"), Gpu.directX, Gpu.openGl, Windows.buildNumber).join(Laptop.cpu).join(Laptop.gpu).join(Laptop.windows)

    df = pd.read_sql(query, con=db.engine)
    df["storage"] = df["ssdStorage"] + df["hddStorage"]
    return df
