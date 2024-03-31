from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/model/{mn}")
def gtm(mn:str):
    if mn=="alexnet":
        return {'sd':'ok'}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name":model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message":"Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/")
async def root():
    return {"message":"hello world!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: int|None = None, short: bool = False):
    item = {"item_id":item_id}
    if not short:
        item.update({"description": "Long product"})
    else:
        item.update({"description":"Short product"})
    if q:
        return item.update({"item_id":item_id, "q":q})
    return item


@app.get("/item/")
async def read_item(product_no: int, limit: int, queue: int=5):
    return {"product_no": product_no + limit + queue}
