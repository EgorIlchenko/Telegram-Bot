from loader import bot
from states.search_info import SearchInfo
from telebot.types import Message
from api import request_info
from utils import info_present
from config_data.config import DATE_FORMAT
from database.models import User, History
from datetime import datetime
import random
from keyboards.reply.reply_keyboard import gen_markup


@bot.message_handler(func=lambda message: message.text == "Низкобюджетные фильмы")
def low_budget_search(message: Message) -> None:
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    bot.send_message(message.from_user.id, 'Сколько фильмов показать?')
    bot.set_state(message.from_user.id, SearchInfo.number_options_low_budget, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_id'] = user_id
        data['film_low_budget'] = f'{random.randrange(500000, 5000000, 100000)}'


@bot.message_handler(state=SearchInfo.number_options_low_budget)
def get_number_options_low_budget(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Вот, что смог найти для Вас:')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['number_options_low_budget'] = message.text

            result_req = request_info.search_film_low_budget(film_low_budget=data['film_low_budget'],
                                                             number_films=data['number_options_low_budget'])
            for film in result_req["docs"]:
                search_result = info_present.key_search(film)
                bot.send_photo(message.from_user.id, search_result["poster"]["url"])
                genres = ", ".join([elem["name"] for elem in search_result["genres"]])
                text = (f"*{search_result["name"]} ({search_result["year"]}), {search_result["ageRating"]}+*\n"
                        f"{"-"*40}\nЖанр: {genres}\n"
                        f"Рейтинг на Кинопоиске: {search_result["rating"]["kp"]}\n"
                        f"Сюжет: {search_result["description"]}\n")
                bot.send_message(message.from_user.id, text, parse_mode='Markdown', reply_markup=gen_markup())
                new_history = History(
                    user_id=data['user_id'],
                    name=search_result["name"],
                    year=search_result["year"],
                    ageRating=search_result["ageRating"],
                    genres=genres,
                    rating=search_result["rating"]["kp"],
                    description=search_result["description"],
                    poster=search_result["poster"]["url"],
                    due_date=datetime.today().strftime(DATE_FORMAT),
                )
                new_history.save()
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Допускаются только цифры!\nСколько фильмов показать?')
