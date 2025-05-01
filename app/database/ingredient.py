from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate, IngredientUpdate


class IngredientCRUD():

    async def get_ingredients(
        self, session: AsyncSession
    ) -> list[Ingredient]:
        ingredients = await session.execute(select(Ingredient))
        return ingredients.scalars().all()

    async def get_ingredient_by_id(
        self,
        indredient_id: int,
        session: AsyncSession
    ) -> Ingredient | None:
        ingredient = await session.execute(
            select(Ingredient).where(Ingredient.id == indredient_id)
        )
        return ingredient.scalar_one_or_none()

    async def get_ingredient_by_name(
        self,
        ingredient_name: str,
        session: AsyncSession
    ) -> Ingredient | None:
        ingredient = await session.execute(
            select(Ingredient).where(Ingredient.name == ingredient_name)
        )
        return ingredient.scalar_one_or_none()

    async def create_ingredient(
        self,
        create_schema: IngredientCreate,
        session: AsyncSession
    ) -> Ingredient:
        new_ingredient = Ingredient(**create_schema.model_dump())
        session.add(new_ingredient)
        await session.commit()
        await session.refresh(new_ingredient)
        return new_ingredient

    async def update_ingredient(
        self,
        update_schema: IngredientUpdate,
        obj_db: Ingredient,
        session: AsyncSession
    ) -> Ingredient:
        setattr(obj_db, 'name', update_schema.name)
        session.add(obj_db)
        await session.commit()
        await session.refresh(obj_db)
        return obj_db


ingredient_crud = IngredientCRUD()
