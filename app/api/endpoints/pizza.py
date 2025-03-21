import json
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.user import current_superuser, current_user
from app.core.db import get_async_session
from app.schemas.pizza import PizzaCreate, PizzaRead, PizzaOrder
from app.validators.pizza import check_duplicate_name, check_exists_pizza
from app.database.pizza import pizza_crud
from app.rabbitmq.pizza import async_rabbitmq
from app.utils.smtp import smtp_server


router = APIRouter(tags=['pizza'], prefix='pizza')


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


@router.get(
    '/info',
    dependencies=[Depends(current_user)],
    response_model=list[PizzaRead],
    response_model_exclude=['id'])
async def get_pizzas(session: AsyncSession = Depends(get_async_session)):
    pizzas_catalog = await pizza_crud.get_all_pizzas(
        session
    )
    return pizzas_catalog


@router.post('/buy_pizza')
async def order_pizza(
        order: PizzaOrder,
        user=Depends(current_user),
        session: AsyncSession = Depends(get_async_session)):
    await check_exists_pizza(order.name, session)
    pizza = await pizza_crud.get_pizza(order.name, session)
    body = {
        'pizza_name': order.name,
        'email': user.email,
        'end_time': (
            datetime.now() + timedelta(minutes=pizza.time)).isoformat()
    }
    await async_rabbitmq.send_message_to_queue(json.dumps(body))
    return JSONResponse(
        {'message': f'DONE! Wait your pizza {pizza.time} minute(s).'},
        status_code=200)
