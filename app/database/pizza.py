from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Pizza
from app.schemas.pizza import PizzaCreate


class PizzaCRUD:
    async def create_pizza(
        self,
        pizza: PizzaCreate,
        session: AsyncSession
    ) -> Pizza:
        new_pizza = Pizza(**pizza.model_dump())
        session.add(new_pizza)
        await session.commit()
        await session.refresh(new_pizza)
        return new_pizza

    async def get_all_pizzas(
        self, session: AsyncSession
    ):
        pizzas = await session.execute(
            select(Pizza)
        )
        return pizzas.scalars().all()


pizza_crud = PizzaCRUD()
