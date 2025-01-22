from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

logging.basicConfig(
    level=logging.INFO, # Уровень логирования, по умолчанию INFO
    format='%(asctime)s - %(levelname)s - %(message)s', # Формат сообщения
    datefmt='%Y-%m-%d %H:%M:%S' # Формат даты
)

log = logging.getLogger(__name__)
class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        print(f"Получено сообщение от {event.from_user.id}: {event.text}")
        log.info(f"Получено сообщение от {event.from_user.id}: {event.text}")
        return await handler(event, data)
