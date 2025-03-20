from pydantic import BaseModel, ConfigDict


class PizzaCreate(BaseModel):
    name: str
    time: str


class PizzaOrder(BaseModel):
    name: str


class PizzaRead(BaseModel):
    id: int
    name: str
    time: str

    model_config = ConfigDict(from_attributes=True)
