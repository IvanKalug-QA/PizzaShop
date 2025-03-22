from app.rabbitmq.pizza import async_rabbitmq


async def check_rabbitmq(ctx):
    await async_rabbitmq.consume_messages_from_queue()
