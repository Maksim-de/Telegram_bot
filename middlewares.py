from aiogram import BaseMiddleware
from aiogram.types import Message

log = {}
class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        print(f"Получено сообщение от {event.from_user.id}: {event.text}")
        return await handler(event, data)