from loader import bot
from telebot.types import Message
from database.models import User, History
from states.search_info import SearchInfo
from typing import List
from keyboards.reply.reply_keyboard import gen_markup


@bot.message_handler(func=lambda message: message.text == "История запросов")
def handle_history(message: Message) -> None:
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    if user is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return
    else:
        bot.set_state(message.from_user.id, SearchInfo.history_date, message.chat.id)
        bot.send_message(message.from_user.id, "За какую дату показать историю?\n"
                                               "_Введите дату в формате: 00.00.0000_", parse_mode='Markdown')


@bot.message_handler(state=SearchInfo.history_date)
def history_result(message: Message) -> None:
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)

    histories: List[History] = user.histories.where(History.due_date == message.text)

    if not histories:
        bot.send_message(message.from_user.id, "История поиска пока пуста!")
        bot.delete_state(message.from_user.id, message.chat.id)
        return

    for film_req in histories:
        bot.send_message(message.from_user.id, f"Дата запроса: *{film_req.due_date}*", parse_mode='Markdown')
        bot.send_photo(message.from_user.id, film_req.poster)
        bot.send_message(message.from_user.id, film_req, parse_mode='Markdown', reply_markup=gen_markup())
    bot.delete_state(message.from_user.id, message.chat.id)
