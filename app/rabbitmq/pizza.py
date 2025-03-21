import json
import asyncio
from datetime import datetime

import aio_pika

from app.core.config import setting
from app.utils.smtp import smtp_server


class RabbitMQAsync:
    async def connect_to_rabbitmq(self):
        connection = await aio_pika.connect_robust(
            setting.rabbitmq_url
        )
        return connection

    async def send_message_to_queue(self, message: str):
        connection = await self.connect_to_rabbitmq()
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=setting.queue_name
            )
            print(f"Sent message: {message} to queue: {setting.queue_name}")

    async def consume_messages_from_queue(self, user_id: int):
        connection = await self.connect_to_rabbitmq()
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(
                setting.queue_name, durable=True)

            async def wait_for_for_message():
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        return message

            try:
                message = await asyncio.wait_for(wait_for_for_message(), 5)
                if message:
                    try:
                        body = message.body.decode()
                        order_data = json.loads(body)
                        pizza_name = order_data['pizza_name']
                        order_email = order_data['email']
                        end_time = datetime.fromisoformat(
                            order_data['end_time'])
                        current_time = datetime.now()
                        if current_time >= end_time:
                            await message.ack()
                            await smtp_server.send_message_order(
                                order_email, pizza_name
                            )
                        else:
                            await message.nack(requeue=True)
                    except Exception:
                        await message.nack(requeue=True)
            except asyncio.TimeoutError:
                return None


async_rabbitmq = RabbitMQAsync()
