from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_bot_commands
from database.models import create_models


if __name__ == '__main__':
    create_models()
    bot.add_custom_filter(StateFilter(bot))
    set_bot_commands(bot)
    bot.infinity_polling()
