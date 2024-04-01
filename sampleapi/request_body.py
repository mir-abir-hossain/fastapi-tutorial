from typing import Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, EmailStr


class Item(BaseModel):
    name: str = Field(examples=['Foo'])
    description: str|None = Field(
        default=None, title="The description of the item", max_length=300, examples=['A very nice Item']
    )
    price: float = Field(
        gt=0, description="The price must be greater than zero", examples=[35.4]
    )
    tax: float|None = Field(examples=[3.2])
    tags: list[str] = []


class UserIn(BaseModel):
    username:str
    password:str
    email: EmailStr
    full_name: str|None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str|None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item)->list[Item]:
    item_dict = item.model_dump()
    if "tax" in item_dict.keys():
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return [item_dict]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)], q: str|None=None):
    result = {"item_id": item_id, "item": item.model_dump()}
    if q:
        result.update({"q":q})
    return result

@app.post("/user/")
async def create_user(user: UserIn)-> UserOut:
    return user