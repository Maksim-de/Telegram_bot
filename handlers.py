from aiogram import Router, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Form, Sport
from api_handler import *
from aiogram.utils.markdown import hbold, hitalic, hunderline, text, code
from config import TOKEN_WEATHER
from datetime import datetime
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

router = Router()

users = {}

food_log = {}
water_log = {}

calorie_burn_rates = {
    "бег": 600,
    "плавание": 500,
    "ходьба": 300,
    "велосипед": 400,
    "силовая": 350,
    "йога": 200,
    "пилатес": 200
}


# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        f"{hbold('🌟 Привет, я твой персональный фитнес-помощник! 🏋️‍♀️')}\n\n"
        f"{hitalic('Я помогу тебе отслеживать твои тренировки и питание,')}\n"
        f"{hitalic('а также следить за прогрессом.')}\n\n"
        f"{hunderline('Мои основные функции:')}\n"
        f"• {hbold('/set_profile')} - {hitalic('Создание профиля пользователя')}\n"
        f"• {hbold('/get_profile')} - {hitalic('Просмотр данных своего профиля')}\n"
        f"• {hbold('/log_water')} - {hitalic('Регистрация количества выпитой воды')}\n"
        f"• {hbold('/log_food')} - {hitalic('Запись калорийности съеденной пищи')}\n"
        f"• {hbold('/log_workout')} - {hitalic('Добавление информации о тренировке')}\n"
        f"• {hbold('/check_progress')} - {hitalic('Просмотр текущего прогресса')}\n"
        f"• {hbold('/info')} - {hitalic('Больше о работе бота')}\n\n"
        f"Для удобной работы со мной можешь воспользоваться меню.\n"
        f"Первым делом создай профиль пользователя {hbold('/set_profile')}"

    )

    await message.answer(welcome_text, parse_mode="HTML")
    # await message.answer_sticker(sticker="CAACAgIAAxkBAAEK7XhlW7jYJ7n9Ym826-0h0w7F8xWk8wACJQoAAgC0uUsjFjL5_7j4rsoE")
    # await message.reply("Добро пожаловать! Я ваш бот.\nВведите /help для списка команд.\n")



# Обработчик команды /info
@router.message(Command("info"))
async def cmd_help(message: Message):
    help_text = (
        f"{hbold('ℹ️ Помощь по использованию бота ℹ️')}\n\n"
        f"{hitalic('Я твой верный помощник в фитнес-достижениях! 💪')}\n\n"
        f"{hunderline('Основные функции:')}\n\n"
        f"🏋️ {hbold('Отслеживание тренировок')}: \n"
        f"   Записывай свои тренировки для отслеживания прогресса. Доступные виды тренировок:\n"
        f"   • {code('бег')}: 600 кал/час\n"
        f"   • {code('плавание')}: 500 кал/час\n"
        f"   • {code('ходьба')}: 300 кал/час\n"
        f"   • {code('велосипед')}: 400 кал/час\n"
        f"   • {code('силовая')}: 350 кал/час\n"
        f"   • {code('йога')}: 200 кал/час\n"
        f"   • {code('пилатес')}: 200 кал/час\n\n"
        f"🥗 {hbold('Отслеживание питания')}: \n"
        f"   Записывай свою еду для контроля калорий. \n"
        f"   Используй команду в формате:\n"
        f"   '/log_food 'название еды' 'вес'\n\n"
        f"💧 {hbold('Мониторинг воды')}:\n"
        f"    Следи за своим водным балансом. \n"
        f"    Используй команду в формате:\n"
        f"    /log_water 'количество воды в мл'\n\n"
        f"📊 {hbold('Просмотр прогресса')}: \n"
        f"   Отслеживай свой ежедневный прогресс. Используй команду '/check_progress'.\n"
        f"   {hitalic('Всегда рад помочь тебе в твоём пути к здоровью! 🌱')}\n"

    )

    await message.answer(help_text, parse_mode="HTML")


# FSM: диалог с пользователем
@router.message(Command("set_profile"))
async def start_form(message: Message, state: FSMContext):
    # await message.answer("Как вас зовут?")
    await message.answer(
        f"👋 {hbold('Привет! Давай познакомимся!')} 😊\n\n"
        f"{hitalic('Для начала, как тебя зовут?')} 📝",
        parse_mode="HTML"
    )
    user_id = message.from_user.id
    users[user_id] = {}
    await state.set_state(Form.name)

def get_gender_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Мужской", callback_data="gender_male"),
            types.InlineKeyboardButton(text="Женский", callback_data="gender_female"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    # await message.answer("Укажите ваш пол:", reply_markup=get_gender_keyboard())
    name = message.text

    await message.answer(
        f"✨ {hbold('Отлично, ' + name + '!')} ✨\n\n"
        f"{hitalic('Теперь укажи, пожалуйста, свой пол:')} 🚻",
        reply_markup=get_gender_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("gender_"))
async def process_gender_callback(query: types.CallbackQuery, state: FSMContext,):
    gender = query.data.split("_")[1]
    if gender == 'male':
        # await query.message.reply("Вы выбрали Мужской")
        await query.message.answer(
            f"💪 {hbold('Отлично, вы выбрали Мужской!')} 👍",
            parse_mode="HTML"
        )
        await state.update_data(gender='Мужской')
    else:
        # await query.message.reply("Вы выбрали Женский")
        await query.message.answer(
            f"💃 {hbold('Прекрасно, вы выбрали Женский!')} 🌸",
            parse_mode="HTML"
        )
        await state.update_data(gender='Женский')
    await query.message.edit_reply_markup(reply_markup=None) #Удаляем кнопки после выбора
    await query.message.answer(
        f"{hitalic('И теперь скажи, сколько тебе лет?')} 🎂",
        parse_mode="HTML"
    )  # Отправляем сообщение
    await state.set_state(Form.age)  # Переходим к следующему состоянию


@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    # await message.answer("В каком городе вы проживаете?")
    await message.answer(f"{hitalic('Cкажи, пожалуйста, из какого ты города?')} 🏙️",
        parse_mode="HTML"
    )
    await state.set_state(Form.city)

@router.message(Form.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer(f"{hitalic('Теперь скажи, пожалуйста, какой у тебя вес?')} ⚖️",
        parse_mode="HTML"
    )
    await state.set_state(Form.weight)

@router.message(Form.weight)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer(f"{hitalic('Отлично! Скажи, пожалуйста, какой у тебя рост?')} 📏",
        parse_mode="HTML"
    )
    await state.set_state(Form.height)

@router.message(Form.height)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await message.answer("Укажите уровень вашей активности", reply_markup=keyboard_lifesyyle())

def keyboard_lifesyyle():
    buttons = [
        [types.InlineKeyboardButton(text="Сидячий и малоподвижный", callback_data="sport_1")],
        [types.InlineKeyboardButton(text="Легкая активность (1-3 раза в неделю)",
                                       callback_data="sport_2")],
        [types.InlineKeyboardButton(text="Средняя активность (3-5 раз в неделю)",
                                       callback_data="sport_3")],
        [types.InlineKeyboardButton(text="Высокая активность (5-7 раз в неделю)",
                                       callback_data="sport_4")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@router.callback_query(F.data.startswith("sport_"))
async def process_gender_callback(query: types.CallbackQuery, state: FSMContext,):
    sport = query.data.split("_")[1]
    # if sport == '1':
    #     await query.message.reply("Вы выбрали Сидячий и малоподвижный")
    #     await state.update_data(lifestyle=1)
    # if sport == '2':
    #     await query.message.reply("Легкая активность (физические упражнения 1-3 раза в неделю)")
    #     await state.update_data(lifestyle=2)
    # if sport == '3':
    #     await query.message.reply("Средняя активность (физические упражнения 3-5 раз в неделю)")
    #     await state.update_data(lifestyle=3)
    # if sport == '4':
    #     await query.message.reply("Высокая активность (физические упражнения 5-7 раз в неделю)")
    #     await state.update_data(lifestyle=4)
    if sport == '1':
        await query.message.answer(
            f"🧘 {hbold('Ты выбрал Сидячий и малоподвижный образ жизни!')} 🛋️",
            parse_mode="HTML"
        )
        await state.update_data(lifestyle=1)
    elif sport == '2':
        await query.message.answer(
            f"🚶 {hbold('Отлично, выбрана Легкая активность (1-3 раза в неделю)!')} 🤸",
            parse_mode="HTML"
        )
        await state.update_data(lifestyle=2)
    elif sport == '3':
        await query.message.answer(
            f"🏃 {hbold('Замечательно, выбрана Средняя активность (3-5 раз в неделю)!')} 🚴",
            parse_mode="HTML"
        )
        await state.update_data(lifestyle=3)
    elif sport == '4':
        await query.message.answer(
            f"🏋️ {hbold('Прекрасно, выбрана Высокая активность (5-7 раз в неделю)!')} 🏆",
            parse_mode="HTML"
        )
        await state.update_data(lifestyle=4)
    # await query.message.edit_reply_markup(reply_markup=None) #Удаляем кнопки после выбора
    await query.message.answer(
        f"{hitalic('И, напоследок, выбери свою цель:')}🎯",
        reply_markup=get_keyboard(),
        parse_mode="HTML"
    )

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Набор массы", callback_data="weight_high"),
            types.InlineKeyboardButton(text="Поддержание веса", callback_data="weight_stogn"),
            types.InlineKeyboardButton(text="Похудение", callback_data="weight_low")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@router.callback_query(F.data.startswith("weight_"))
async def callbacks_num(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    age = float(data.get("age"))
    lifestyle = data.get("lifestyle")
    gender = data.get("gender")
    weight = float(data.get("weight"))
    height = float(data.get("height"))
    city = data.get("city")
    action = callback.data
    if gender == 'Мужской':
        target = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        target = 447.6 + (9.2 * weight) + (3.1 * height) -(4.3 * age)
    if lifestyle == 1:
        norma = target *1.2
        await state.update_data(norma=norma)
    elif lifestyle == 2:
        norma = target * 1.375
        await state.update_data(norma=norma)
    elif lifestyle == 3:
        norma = target * 1.55
        await state.update_data(norma=norma)
    elif lifestyle == 4:
        norma = target * 1.725
        await state.update_data(norma=norma)
    if action == "weight_high":
        target = norma + 450
        activity = "Набор веса"
        await state.update_data(activity=activity)
        await state.update_data(target=target)
    elif action == "weight_stogn":
        target = norma
        activity = "Поддержание веса"
        await state.update_data(activity=activity)
        await state.update_data(target=target)
    else:
        target = norma - 450
        activity = "Похудение/сушка"
        await state.update_data(activity=activity)
        await state.update_data(target=target)
    print(city)
    temp_now = await api_request(TOKEN_WEATHER, city)
    water = weight * 30
    print("Температура в ", city, temp_now)
    if temp_now > 20:
        water+=500
    await state.update_data(water=water)
    # await callback.message.edit_reply_markup(reply_markup=None)  # Удаляем кнопки после выбора
    response_text = text(
        f"👤 {hbold('Имя:')} {name}\n",
        f"🎂 {hbold('Возраст:')} {int(age)}\n",
        f"🚻 {hbold('Пол:')} {gender}\n",
        f"📏 {hbold('Рост:')} {height} см\n",
        f"⚖️ {hbold('Вес:')} {weight} кг\n",
        f"🎯 {hbold('Ваша цель:')} {activity}\n",
        f"🔥 {hbold('Целевое количество калорий:')} {int(target)}\n",
        f"💧 {hbold('Требуемое количество жидкости:')} {int(water)} мл",
        sep="\n"
    )
    await callback.message.answer(response_text, parse_mode="HTML")
    # await callback.message.answer(response_text)
    user_id = callback.from_user.id
    users[user_id]['name'] = name
    users[user_id]['age'] = age
    users[user_id]['weight'] = weight
    users[user_id]['height'] = height
    users[user_id]['gender'] = gender
    users[user_id]['norma'] = norma
    users[user_id]['activity'] = activity
    users[user_id]['target'] = target
    users[user_id]['water'] = water
    users[user_id]['city'] = city
    users[user_id]['water_now'] = int(0)
    users[user_id]['target_now'] = int(0)
    users[user_id]['burn'] = int(0)
    await state.clear()

@router.message(Command("log_water"))
async def log_water(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if len(message.text.split()) == 1:
        await message.reply(
            f"💧 {hitalic('Пожалуйста, введи количество выпитой воды в миллилитрах (мл).')}\n"
            f"   {hbold('Пример:')} /log_water 250",
            parse_mode="HTML"
        )
    else:
        try:
            water_now = int(message.text.split()[1])
            users[user_id]['water_now'] += water_now
            # Добавили
            if 'water_log' not in users[user_id]:
                users[user_id]['water_log'] = []
            users[user_id]['water_log'].append(
                {"time": datetime.now(), "amount": water_now}
            )
            await message.reply(
                 f"✅ {hbold('Отлично! Ты выпил(а)')} {hbold(f'{water_now} мл')} 💧\n"
                 f"{hitalic('Твой прогресс: ')} {users[user_id]['water_now']}/{users[user_id]['water']} мл",
                parse_mode="HTML"
                )
        except(ValueError, KeyError):
            await message.reply(
                f"⚠️ {hitalic('Произошла ошибка! Пожалуйста, проверь формат ввода.')}\n"
                f"   {hbold('Пример:')} /log_water 250",
                parse_mode="HTML"
            )


@router.message(Command("log_food"))
async def log_food(message: Message):
    user_id = message.from_user.id
    mess = message.text
    text_to_translate = mess[9:len(mess)]
    if not text_to_translate:
        await message.reply(
            f"🥗 {hitalic('Пожалуйста, введи название продукта и его вес.')}\n"
            f"   {hbold('Пример:')} /log_food Яблоко 150 грамм",
            parse_mode="HTML"
        )
        return
    calories, totalweight = await caloric(text_to_translate)
    await message.answer(
            f"🍽️ {hbold('Записано!')} {hitalic(text_to_translate)} \n"
            f"   {hbold('Калорийность:')} {int(calories)} ккал\n"
            f"   {hbold('Вес:')} {int(totalweight)} г",
             parse_mode="HTML"
        )
    # Добавили для визуализации
    if 'food_log' not in users[user_id]:
        users[user_id]['food_log'] = []
    users[user_id]['food_log'].append(
        {"time": datetime.now(), "calories": calories, "weight": totalweight}
    )
    users[user_id]['target_now'] = users[user_id]['target_now'] + calories
    if users[user_id]['target_now'] < users[user_id]['target']:
        await message.reply(
               f"✅ {hbold('Отлично! Твой прогресс:')} {int(users[user_id]['target_now'])}/{int(users[user_id]['target'])} ккал\n"
               f"   {hitalic('Ты молодец! Продолжай в том же духе! 💪')}",
               parse_mode="HTML"
            )
    else:
        await message.reply(
                f"⚠️ {hbold('Внимание! Твой прогресс:')} {int(users[user_id]['target_now'])}/{int(users[user_id]['target'])} ккал\n"
                f"   {hitalic('Кажется, пора остановиться! 🙅‍♂️')}",
                parse_mode="HTML"
            )

def create_workout_keyboard():
    buttons = []
    for workout_type in calorie_burn_rates.keys():
        buttons.append([types.InlineKeyboardButton(text=workout_type, callback_data=f"workout_{workout_type}")])
        # buttons.append(types.InlineKeyboardButton(text=workout_type, callback_data=f"workout_{workout_type}"))
    # keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@router.message(Command("log_workout"))
async def log_sport(message: Message,state: FSMContext):
    keyboard = create_workout_keyboard()
    await message.answer(
        f"{hbold('🏋️ Выбери вид тренировки:')}\n\n"
        f"{hitalic('Нажми на кнопку ниже, чтобы выбрать тип тренировки')}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("workout_"))
async def process_sport_callback(query: types.CallbackQuery, state: FSMContext):
    sport = query.data.split("_")[1]
    await state.set_state(Sport.sport)
    await state.update_data(sport=sport)
    await query.message.reply(
        f"⏱️{hitalic('Укажи длительность тренировки в минутах:')}",
        parse_mode="HTML"
    )
    await state.set_state(Sport.time)

@router.message(Sport.time)
async def process_sport(message: Message, state: FSMContext):
    try:
        await state.update_data(time=message.text)
        data = await state.get_data()
        sport = data.get("sport")
        min = message.text
        calories = int(calorie_burn_rates[sport])* (int(min)/60)
        user_id = message.from_user.id
        users[user_id]['burn'] += int(calories)
        await message.reply(
            f"🔥 {hbold('Отлично, ты сжег')} {hbold(f'{int(calories)} ккал')}!\n"
            f"   {hitalic('Суммарно сожжено:')} {users[user_id]['burn']} ккал",
            parse_mode="HTML"
        )
        if int(min) > 30:
            users[user_id]['water'] = int(users[user_id]['water']) + 250
            await message.reply(
                f"🔥 {hbold('Длительная тренировка - выпей дополнительно 250 мл воды')}!\n"
                f"   {hitalic('Дневная норма увеличена до :')} {users[user_id]['water']} мл",
                parse_mode="HTML"
            )
    except (ValueError, KeyError) as e:
        await message.answer(
            f"⚠️ {hitalic('Произошла ошибка! Пожалуйста, проверьте корректность ввода времени.')}\n"
            f"    {hbold('Пример:')} 30",
            parse_mode="HTML"
        )
    await state.clear()

@router.message(Command("get_profile"))
async def get_profile(message: Message):
    user_id = message.from_user.id
    name = users[user_id]['name']
    age = users[user_id]['age']
    weight = users[user_id]['weight']
    height = users[user_id]['height']
    gender = users[user_id]['gender']
    norma = users[user_id]['norma']
    activity = users[user_id]['activity']
    target = users[user_id]['target']
    water = users[user_id]['water']
    city = users[user_id]['city']
    water_now = users[user_id]['water_now']
    target_now = users[user_id]['target_now']
    burn = users[user_id]['burn']
    response_text = text(
        f"👤 {hbold('Имя:')} {name}\n",
        f"🎂 {hbold('Возраст:')} {age}\n",
        f"🚻 {hbold('Пол:')} {gender}\n",
        f"📏 {hbold('Рост:')} {height} см\n",
        f"⚖️ {hbold('Вес:')} {weight} кг\n",
        f"🎯 {hbold('Ваша цель:')} {activity}\n",
        f"🔥 {hbold('Целевое количество калорий:')} {int(target)}\n",
        f"💧 {hbold('Требуемое количество жидкости:')} {int(water)} мл\n",
        f"🏙️ {hbold('Город:')} {city}\n",
        f"💧 {hbold('Выпито воды:')} {water_now} мл\n",
        f"🍽️ {hbold('Съедено калорий:')} {int(target_now)} ккал\n",
        f"🏋️ {hbold('Сожжено калорий:')} {burn} ккал",
        sep="\n"
    )
    await message.reply(response_text, parse_mode="HTML")

@router.message(Command("check_progress"))
async def check_progress(message: Message):
    user_id = message.from_user.id
    if user_id not in users or not users[user_id]:
        await message.reply(
            f"⚠️ {hitalic('Профиль не найден! Пожалуйста, сначала заполните его командой /set_profile.')}",
            parse_mode="HTML"
        )
        return

    user_data = users[user_id]
    name = user_data.get('name', 'не указано')
    norma = user_data.get('norma', 'не указано')
    target = user_data.get('target', 'не указано')
    water = user_data.get('water', 'не указано')
    water_now = user_data.get('water_now', 0)
    target_now = user_data.get('target_now', 0)
    burn = user_data.get('burn', 0)
    activity = user_data.get('activity', 'не указано')

    if water != 'не указано' and int(water) > 0:
        water_percentage = (water_now / int(water)) * 100
    else:
        water_percentage = 0

    if target != 'не указано' and float(target) > 0:
        target_percentage = (target_now / float(target)) * 100
    else:
        target_percentage = 0
    response_text = text(
        f"📊 {hbold('Твой прогресс, ' + name + '!')}\n\n",
        f"🎯 {hbold('Твоя цель:')} {activity}\n",
        f"🔥 {hbold('Цель по калориям:')} {int(target)} ккал\n",
        f"💧 {hbold('Норма воды:')} {int(water)} мл\n",
        f"💧 {hbold('Выпито воды:')} {water_now} мл ({water_percentage:.1f}%)\n",
        f"🍽️ {hbold('Съедено калорий:')} {int(target_now)} ккал ({target_percentage:.1f}%)\n",
        f"🏋️ {hbold('Сожжено калорий:')} {burn} ккал",
        sep="\n"
    )
    await message.reply(response_text, parse_mode="HTML")

@router.message(Command("get_chart"))
async def check_progress(message: Message):
    user_id = message.from_user.id
    # Построение и отправка графика
    buf = await plot_daily_progress(user_id)
    if buf:
        await message.answer_photo(
            photo=types.BufferedInputFile(buf.read(), filename="daily_progress.png")
        )
    else:
        await message.reply("Нет данных для построения графика.")


def get_water_log(user_id):
    if user_id in users and 'water_log' in users[user_id]:
        return users[user_id]['water_log']
    else:
        return []

def get_food_log(user_id):
    if user_id in users and 'food_log' in users[user_id]:
        return users[user_id]['food_log']
    else:
        return []



async def plot_daily_progress(user_id):
    water_log = get_water_log(user_id)
    food_log = get_food_log(user_id)

    if not water_log and not food_log:
        return None

    # Получаем текущую дату
    today = datetime.now().date()

    # Подготавливаем данные для графиков
    water_times = []
    water_amounts = []
    cumulative_water = 0
    for log in water_log:
        if isinstance(log, dict) and 'time' in log and 'amount' in log and isinstance(log['amount'], (int, float)):
             if log['time'].date() == today:
                cumulative_water += log['amount']
                water_times.append(log['time'])
                water_amounts.append(cumulative_water)
             else:
                 print(f"Warning: Invalid water log entry: {log}")


    food_times = []
    food_calories = []
    cumulative_calories = 0
    for log in food_log:
        if isinstance(log, dict) and 'time' in log and 'calories' in log and isinstance(log['calories'], (int, float)):
             if log['time'].date() == today:
                cumulative_calories += log['calories']
                food_times.append(log['time'])
                food_calories.append(cumulative_calories)
        else:
            print(f"Warning: Invalid food log entry: {log}")


    # Создаем фигуру и ось
    fig, ax = plt.subplots(figsize=(10, 6))

    # График для воды
    if water_times:
        ax.plot(water_times, water_amounts, color='blue', label='Вода (мл)')

    # График для калорий
    if food_times:
        ax.plot(food_times, food_calories, color='red', label='Калории (ккал)')


    # Форматирование оси X
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlabel('Время (часы)')
    ax.tick_params(axis='x', rotation=45)

    # Добавляем общую легенду
    ax.legend(loc='upper left')

    # Задаем временные границы
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    ax.set_xlim(start_of_day, end_of_day)
    ax.set_ylabel('Сумма воды (мл) / Сумма калорий (ккал)')
    fig.tight_layout()

    # Сохраняем график в буфер памяти
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return buf

@router.message(Command("new_day"))
async def new_day(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
          await message.reply(
            f"⚠️ {hitalic('Профиль не найден! Пожалуйста, сначала заполните его командой /set_profile.')}",
            parse_mode="HTML"
        )
          return
    users[user_id]['water_now'] = 0
    users[user_id]['target_now'] = 0
    users[user_id]['burn'] = 0
    weight = users[user_id]['weight']
    city = users[user_id]['city']
    temp_now = await api_request(TOKEN_WEATHER, city)
    water = weight * 30
    print("Температура в ", city, temp_now)
    if temp_now > 20:
        water += 500
    users[user_id]['water'] = water

    await message.reply(
        f"✅ {hbold('Все достижения за день обнулены! Готов к новым свершениям!')}",
        parse_mode="HTML"
    )