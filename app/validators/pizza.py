from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models import Pizza


async def check_duplicate_name(name: str, session: AsyncSession):
    pizza = await session.execute(
        select(Pizza.name).where(Pizza.name == name)
    )
    pizza = pizza.scalar_one_or_none()
    if pizza is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='This pizza exists!'
        )
