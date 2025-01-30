from telebot.types import Message
from loader import bot
from peewee import IntegrityError
from database.models import User
from keyboards.reply.reply_keyboard import gen_markup


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        User.create(
            user_id=user_id,
            username=username,
        )
        bot.send_message(message.from_user.id, "Добро пожаловать в поисковик фильмов!",
                         reply_markup=gen_markup())
    except IntegrityError:
        bot.send_message(message.from_user.id, f"Рад вас снова видеть, *{username}*!",
                         parse_mode='Markdown',
                         reply_markup=gen_markup())
