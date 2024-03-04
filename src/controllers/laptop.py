# import pandas as pd
# from sqlalchemy import select
# from  import engine
# from src.models.models import Laptop, Cpu, Gpu, Windows


class LaptopController():
    @staticmethod
    def test():
        return {"status": "success"}
#     @staticmethod
#     def get_all():
#         laptops = pd.read_sql(select(Laptop, Cpu, Gpu, Windows).join(
#             Laptop.cpu).join(Laptop.gpu).join(Laptop.windows), engine)
#         laptop_json = laptops.to_dict(orient="records")

#         return {"message": "success", "laptops": laptop_json}
