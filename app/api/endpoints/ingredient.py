from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.ingredient import (
    IngredientCreate, IngredientUpdate,
    IngredientDB)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.database.ingredient import ingredient_crud
from app.validators.ingredient import (
    check_ingredient_on_unique,
    get_ingredient_by_id_or_404)


router = APIRouter(tags=['ingredients(For Admin)'])


@router.get(
    '/',
    response_model=list[IngredientDB],
    dependencies=[Depends(current_superuser)])
async def get_all_ingredients(
    session: AsyncSession = Depends(get_async_session)
):
    ingredients = await ingredient_crud.get_ingredients(session)
    return ingredients


@router.post(
    '/',
    response_model=IngredientDB,
    dependencies=[Depends(current_superuser)]
)
async def create_ingredient(
    ingredient_schema: IngredientCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_ingredient_on_unique(
        ingredient_schema.name, session, ingredient_crud)
    ingredient = await ingredient_crud.create_ingredient(
        ingredient_schema, session
    )
    return ingredient


@router.patch(
    '/{id}',
    response_model=IngredientDB,
    dependencies=[Depends(current_superuser)]
)
async def update_ingredient(
    id: int,
    ingredient_update: IngredientUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    obj_db = await get_ingredient_by_id_or_404(
        id, session, ingredient_crud
    )
    update_ingredient_db = await ingredient_crud.update_ingredient(
        ingredient_update, obj_db, session
    )
    return update_ingredient_db
