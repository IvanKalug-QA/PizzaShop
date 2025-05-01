from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ingredient import Ingredient


async def check_ingredient_on_unique(
    ingredient_name: str,
    session: AsyncSession,
    ingredient_crud
) -> None:
    ingredient = await ingredient_crud.get_ingredient_by_name(
        ingredient_name, session
    )
    if ingredient is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Такой ингредиент уже есть!'
        )


async def get_ingredient_by_id_or_404(
    ingredient_id: int,
    session: AsyncSession,
    ingredient_crud
) -> Ingredient:
    ingredient = await ingredient_crud.get_ingredient_by_id(
        ingredient_id, session
    )
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такого ингредиента нет!'
        )
    return ingredient
