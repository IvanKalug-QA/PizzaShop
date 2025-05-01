from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

PizzaIngredient = Table(
    'pizza_ingredient',
    Base.metadata,
    Column(
        'pizza_id',
        ForeignKey('pizza.id'),
        primary_key=True,
        nullable=False
    ),
    Column(
        'ingredient_id',
        ForeignKey('ingredient.id'),
        primary_key=True,
        nullable=False
    )
)


class Pizza(Base):
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    time: Mapped[int] = mapped_column(Integer, nullable=False)
    ingredients: Mapped[list['Ingredient']] = relationship(
        'Ingredient', secondary=PizzaIngredient, back_populates='pizzas'
    )
