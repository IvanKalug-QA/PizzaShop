from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.database.pizza import pizza_crud


async def check_duplicate_name(name: str, session: AsyncSession):
    pizza = await pizza_crud.get_pizza(name, session)
    if pizza is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='This pizza exists!'
        )


async def check_exists_pizza(name: str, session: AsyncSession):
    pizza = await pizza_crud.get_pizza(name, session)
    if pizza is None:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail='This pizza is not exists!'
        )
