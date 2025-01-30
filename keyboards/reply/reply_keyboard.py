from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def gen_markup():
    button_1 = KeyboardButton(text="Поиск по названию")
    button_2 = KeyboardButton(text="Поиск по жанру")
    button_3 = KeyboardButton(text="Поиск по рейтингу")
    button_4 = KeyboardButton(text="Низкобюджетные фильмы")
    button_5 = KeyboardButton(text="Высокобюджетные фильмы")
    button_6 = KeyboardButton(text="История запросов")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    keyboard.add(button_2)
    keyboard.add(button_3)
    keyboard.add(button_4)
    keyboard.add(button_5)
    keyboard.add(button_6)

    return keyboard
