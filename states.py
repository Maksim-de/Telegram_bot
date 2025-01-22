from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    gender = State()
    age = State()
    city = State()
    weight = State()
    height = State()
    lifestyle = State()
    activity = State()
    norma = State()
    target = State()
    water = State()
    water_now = State()
    target_now = State()

class Sport(StatesGroup):
    sport = State()
    time = State()

