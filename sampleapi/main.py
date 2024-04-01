from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Path, Query, Response
from fastapi.responses import JSONResponse

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


@app.get("/itemms/")
async def read_items(q: Annotated[str, Query(max_length=50)]=None):
    results = {"items":[{"item_id":"Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q":q})
    return results

@app.get("/ittemms/", response_model=None)
async def read_ittemms(q: Annotated[list[str], Query()]=None)->Response|dict:
    results = {"items":[{"item_id":"Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q":q})
    return JSONResponse(content={"message":"ok", "content":results})

@app.get("/itemss/{item_id}")
async def get_itemss(item_id: Annotated[int, Path(ge=3)]):
    return item_id
