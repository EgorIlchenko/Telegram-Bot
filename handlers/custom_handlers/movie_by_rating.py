from loader import bot
from states.search_info import SearchInfo
from telebot.types import Message
from api import request_info
from utils import info_present
from config_data.config import DATE_FORMAT
from database.models import User, History
from datetime import datetime
from keyboards.reply.reply_keyboard import gen_markup


@bot.message_handler(func=lambda message: message.text == "Поиск по рейтингу")
def rating_search(message: Message) -> None:
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    bot.set_state(message.from_user.id, SearchInfo.film_rating, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите рейтинг для поиска _(Пример: 4, 5, 6-7)_', parse_mode='Markdown')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_id'] = user_id


@bot.message_handler(state=SearchInfo.film_rating)
def get_film_rating(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Сколько фильмов показать?')
    bot.set_state(message.from_user.id, SearchInfo.number_options_rating, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['film_rating'] = str(message.text)


@bot.message_handler(state=SearchInfo.number_options_rating)
def get_number_options_rating(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Вот, что смог найти для Вас:')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['number_options_rating'] = message.text

            result_req = request_info.search_film_rating(film_rating=data['film_rating'],
                                                         number_films=data['number_options_rating'])
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
