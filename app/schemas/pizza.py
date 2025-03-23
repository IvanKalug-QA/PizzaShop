from pydantic import BaseModel, ConfigDict


class PizzaCreate(BaseModel):
    name: str
    time: int


class PizzaOrder(BaseModel):
    name: str


class PizzaRead(BaseModel):
    id: int
    name: str
    time: int

    model_config = ConfigDict(from_attributes=True)
