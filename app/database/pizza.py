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
    ) -> list[Pizza]:
        pizzas = await session.execute(
            select(Pizza)
        )
        return pizzas.scalars().all()

    async def get_pizza(
        pizza_name: str,
        session: AsyncSession
    ) -> Pizza | None:
        pizza = await session.execute(
            select(Pizza).where(Pizza.name == pizza_name)
        )
        return pizza.scalar_one_or_none()


pizza_crud = PizzaCRUD()
