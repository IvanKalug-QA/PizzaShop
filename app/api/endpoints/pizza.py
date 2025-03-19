from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.user import current_superuser
from app.core.db import get_async_session
from app.schemas.pizza import PizzaCreate, PizzaRead
from app.validators.pizza import check_duplicate_name
from app.database.pizza import pizza_crud


router = APIRouter(tags=['pizza'])


@router.post(
        '/',
        dependencies=[Depends(current_superuser),],
        response_model=PizzaRead
        )
async def add_pizza(
        pizza: PizzaCreate,
        session: AsyncSession = Depends(get_async_session)):
    await check_duplicate_name(pizza.name, session)
    new_pizza = await pizza_crud.create_pizza(pizza, session)
    return new_pizza
