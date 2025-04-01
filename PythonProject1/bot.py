# Імпорти з aiogram
import types

import executor
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils import keyboard

# Імпорти з інших файлів
from commands import *
# Імпорт токена
from config import BOT_TOKEN as TOKEN
from data import get_films, add_film
from keyboards import films_keyboard_markup, FilmCallback
from logger import logger
from models import Film
from states import *

button = InlineKeyboardButton(
    text="Some Film Name",
    callback_data=
    FilmCallback.new(id=1, name="Some Film Name")  # Використовуємо film_callback.new()
)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Створення екземпляра диспетчера з використанням ключового слова bot
  # Виправлений спосіб ініціалізації Dispatcher

film_callback = CallbackData()

@dp.message(EDIT_FILMS_COMMAND)
async def edit_film(message: Message, state: FSMContext) -> None:
    await state.set_state(FilmEdit.edit_query)
    await message.answer(
        "Ведіть назву для пошуку",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(SEARCH_FILMS_COMMAND)
async def search_film(message: Message, state: FSMContext) -> None:
    await state.set_state(FilmSort.search_query)
    await message.answer(
        'Введіть назву фільму для пошуку',
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(FilmSort.search_query)
async def search_query(message: Message, state: FSMContext) -> None:
    query = message.text.lower()
    movies = get_films()
    results = [film for film in movies if query in film['name'].lower()]
    if results:
        await message.reply('Пошук виконаний!', reply_markup=films_keyboard_markup(results))
    else:
        await message.reply('Пошук не вдався'),
    await state.clear()

@dp.message(FILTER_FILMS_COMMAND)
async def filter_films (message: Message, state: FSMContext) -> None:
        await state.set_state(FilmFilter.filter_criteria)
        await message.answer(
               f"Введіть жанр / рік для фільтрації",
               reply_markup=ReplyKeyboardRemove(),
        )

@dp.message(FilmFilter.filter_criteria)
async def filter_criteria(message: Message, state: FSMContext) -> None:
    criteria = message.text.lower()
    all_films = get_films()
    result = [film for film in all_films if criteria in film["genre"].lower() or criteria == film["rating"]]
    if result:
        await message.reply(
            f"Цей фільм знайдено!",
            reply_markup=films_keyboard_markup(result)
        )
    else:
        await message.reply(
            f"Нічого не знайдено:("),
    await state.clear()





@dp.message(FILM_CREATE_COMMAND)
async def film_create(message: Message, state: FSMContext) -> None:
    await state.set_state(FilmForm.name)
    await message.answer(
        f"Введіть назву фільму.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.name)
async def film_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(FilmForm.description)
    await message.answer(
        f"Введіть опис фільму.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.description)
async def film_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer(
        f"Вкажіть рейтинг фільму від 0 до 10.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.rating)
async def film_rating(message: Message, state: FSMContext) -> None:
    await state.update_data(rating=float(message.text))
    await state.set_state(FilmForm.genre)
    await message.answer(
        f"Введіть жанр фільму.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.genre)
async def film_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(FilmForm.actors)
    await message.answer(
        text=f"Введіть акторів фільму через роздільник ', '\n"
             + html.bold("Обов'язкова кома та відступ після неї."),
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.actors)
async def film_actors(message: Message, state: FSMContext) -> None:
    await state.update_data(actors=[x for x in message.text.split(", ")])
    await state.set_state(FilmForm.poster)
    await message.answer(
        f"Введіть посилання на постер фільму.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.poster)
async def film_poster(message: Message, state: FSMContext) -> None:
    data = await state.update_data(poster=message.text)
    film = Film(**data)
    add_film(film.model_dump())
    await state.clear()
    await message.answer(
        f"Фільм {film.name} успішно додано!",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(Command("start"))
async def start(message: Message) -> None:
    logger.debug("Hello")
    await message.answer(
        f"Вітаю, {message.from_user.full_name}!\n"
        "Я перший бот Python розробника Тарнавського Павла."
    )

    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(FILMS_COMMAND)
async def films(message: Message) -> None:
    data = get_films()
    markup = films_keyboard_markup(films_list=data)
    await message.answer(
        f"Перелік фільмів. Натисніть на назву фільму для отримання деталей.",
        reply_markup=markup
    )

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")




@dp.callback_query(FilmCallback.filter())
async def callback_film(callback: CallbackQuery, callback_data: dict) -> None:
    film_id = callback_data["id"]
    film_name = callback_data["name"]

    # Ваш код для обробки callback-даних
    await callback.message.answer(f"Фільм: {film_name}, ID: {film_id}")

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Виберіть фільм:", reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('film_'))
async def callback_film(callback: CallbackQuery) -> None:
    # Отримуємо дані callback
    callback_data = film_callback.parse(callback.data)

    film_id = callback_data["id"]
    film_name = callback_data["name"]

    # Відправляємо відповідь з даними фільму
    await callback.message.answer(f"Фільм: {film_name}, ID: {film_id}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)