from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.pizza import PizzaIngredient


class Ingredient(Base):
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    pizza: Mapped[list['Pizza']] = relationship(
        'Ingredient', secondary=PizzaIngredient,
        back_populates='ingredients'
    )

    def __repr__(self):
        return f'{self.name}'
