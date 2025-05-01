from pydantic import BaseModel, ConfigDict


class IngredientCreate(BaseModel):
    name: str


class IngredientUpdate(IngredientCreate):
    pass


class IngredientDB(IngredientCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
