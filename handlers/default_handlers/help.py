from telebot.types import Message
from loader import bot
from config_data.config import DEFAULT_COMMANDS
from keyboards.reply.reply_keyboard import gen_markup


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'Список доступных команд:\n/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.from_user.id, '\n'.join(text), reply_markup=gen_markup())
