from aiogram.utils.keyboard import InlineKeyboardBuilder

# Клас для роботи з callback_data
class FilmCallback:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def pack(self):
        # Пакуємо дані в callback_data для кнопки
        return f"film_{self.id}"

    @classmethod
    def unpack(cls, data):
        # Розпаковуємо callback_data і отримуємо id
        film_id = int(data.split("_")[1])
        return cls(id=film_id, name=f"Film {film_id}")

    @classmethod
    def filter(cls):
        pass

    @classmethod
    def new(cls, id, name):
        pass


# Функція для створення клавіатури з фільмами
def films_keyboard_markup(films_list):
    builder = InlineKeyboardBuilder()

    # Додаємо кнопки для кожного фільму
    for index, film_data in enumerate(films_list):
        callback_data = FilmCallback(id=index, **film_data)  # Створюємо об'єкт FilmCallback
        builder.button(
            text=f"{callback_data.name}",  # Текст на кнопці
            callback_data=callback_data.pack()  # Пакуємо callback_data
        )

    builder.adjust(1, repeat=True)  # Розміщуємо кнопки одна під одною
    return builder.as_markup()