# commands.py - модуль в якому оголошені всі необхідні команди(та їх фільтри)
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

FILMS_COMMAND = Command('films')
START_COMMAND = Command('start')
FILM_CREATE_COMMAND = Command("create_film")
SEARCH_FILMS_COMMAND = Command('search_film')
FILTER_FILMS_COMMAND = Command('filter_films')
EDIT_FILMS_COMMAND = Command('delete_film')

BOT_COMMANDS = [
   BotCommand(command="films", description="Перегляд списку фільмів"),
   BotCommand(command="start", description="Почати розмову"),
   BotCommand(command="create_film", description="Додати новий фільм"),
   BotCommand(command='search_film', description="Пошук фільму"),
   BotCommand(command='filter_movies',description="Фільтрація фільмів"),
   BotCommand(command="delete_film", description="Видалити фільм"),

]