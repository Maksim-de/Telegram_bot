import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Чтение токена из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
TOKEN_WEATHER = os.getenv("OPEN_API_WEATHER")
API_EDA = os.getenv("API_KEY")

if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")
if not TOKEN_WEATHER:
    raise ValueError("Переменная окружения TOKEN_WEATHER не установлена!")