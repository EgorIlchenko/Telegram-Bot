from telebot.handler_backends import State, StatesGroup


class SearchInfo(StatesGroup):
    film_name = State()
    film_rating = State()
    film_genre = State()
    number_options = State()
    number_options_rating = State()
    number_options_genre = State()
    number_options_low_budget = State()
    number_options_high_budget = State()
    history_date = State()
