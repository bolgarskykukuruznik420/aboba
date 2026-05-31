from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

def categories_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📱 Телефоны",
        callback_data="cat_phones"
    )

    builder.button(
        text="🍎 iPhone",
        callback_data="cat_iphone"
    )

    builder.button(
        text="🤖 Samsung",
        callback_data="cat_samsung"
    )

    builder.button(
        text="💻 Ноутбуки",
        callback_data="cat_laptops"
    )

    builder.button(
        text="🎮 PS5",
        callback_data="cat_ps5"
    )
    builder.button(
        text="🔎 Поиск по слову",
        callback_data="cat_search"
    )
    builder.adjust(1)

    return builder.as_markup()


def condition_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🆕 Новое",
        callback_data="cond_2"
    )

    builder.button(
        text="📦 Б/У",
        callback_data="cond_1"
    )

    builder.adjust(1)

    return builder.as_markup()


def main_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="➕ Создать фильтр"
                )
            ],
            [
                KeyboardButton(
                    text="📋 Мои фильтры"
                )
            ],
            [
                KeyboardButton(
                    text="❌ Удалить фильтр"
                )
            ],
            [
                KeyboardButton(
                    text="✅ Выбрать фильтр"
                )
            ]
        ],
        resize_keyboard=True
    )