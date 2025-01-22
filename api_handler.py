import aiohttp
import asyncio
from config import *
from yandex_cloud_ml_sdk import YCloudML

async def api_request(TOKEN_WEATHER, option):
    if TOKEN_WEATHER != '':
        params = {'q': option, 'appid': TOKEN_WEATHER, 'units': 'metric', 'lang': 'ru'}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('https://api.openweathermap.org/data/2.5/weather', params=params) as response:
                    if response.status == 200:
                        print('Ключ применен успешно')
                        data = await response.json()
                        print(option, data['main']['temp'])
                        return float(data['main']['temp'])
                    else:
                        error_data = await response.json()
                        print('Ошибка')
                        return 0
            except aiohttp.ClientError as e:
                print(f"Ошибка запроса: {e}")
                print('Произошла ошибка при выполнении запроса к API.')
                return 0

# Замените на ваши ключи API
APP_ID = "423af06d"
APP_KEY = "1e5049cbe9ed1862147ff5346fcc4564"


async def analyze_ingredient(session, query):
    """Асинхронно анализирует ингредиент, используя API Edamam Nutrition Data.

    Args:
        session: aiohttp.ClientSession.
        query: Строка ингредиента для анализа.

    Returns:
        JSON: Ответ API Edamam или None в случае ошибки.
    """
    url = "https://api.edamam.com/api/nutrition-data"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "ingr": query,
        "nutrition-type": "cooking"  # По умолчанию, можно изменить на "logging"
    }
    try:
        async with session.get(url, params=params) as response:
            response.raise_for_status()  # Проверяем, что запрос успешен (статус 200)
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе API: {e}")
        return None





async def translate_text(session, text):
    """Асинхронно переводит текст, используя API Mymemory.

    Args:
        session: aiohttp.ClientSession.
        text: Текст для перевода.
        langpair: Пара языков.

    Returns:
        JSON: Ответ API.
    """
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair=ru|en"
    print(url)
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Проверяем, что запрос успешен (статус 200)
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе API: {e}")
        return None

async def caloric(text_to_translate):
    """Основная асинхронная функция для управления запросами."""
    async with aiohttp.ClientSession() as session:
        source_language = "ru"
        target_language = "en"
        translation_result = await translate_text(session, text_to_translate)
        print(translation_result['responseData']['translatedText'])
        translation_result = translation_result['responseData']['translatedText']
        ingredient_info = await analyze_ingredient(session, translation_result)
        print(ingredient_info)
        print("Калории: ", ingredient_info['calories'])
        print("Вес: ", ingredient_info['totalWeight'])
        calories = ingredient_info['calories']
        totalWeight = ingredient_info['totalWeight']
        return calories, totalWeight





# if __name__ == "__main__":
#   asyncio.run(main())