import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from data import delete_filter
from config import BOT_TOKEN
from states import CreateFilter
from keyboards import (
    categories_keyboard,
    condition_keyboard,
    main_keyboard
)
from data import add_filter, get_filters
from kufar_parser import get_items
from data import set_active_filter
from data import (
    add_filter,
    get_filters,
    get_all_filters,
    get_active_filters,
    is_seen,
    add_seen
)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "Выберите действие:",
        reply_markup=main_keyboard()
    )

@dp.message(F.text == "➕ Создать фильтр")
async def create_filter(message: Message, state: FSMContext):

    await state.set_state(CreateFilter.choosing_category)

    await message.answer(
        "Выбери категорию:",
        reply_markup=categories_keyboard()
    )
@dp.message(F.text == "❌ Удалить фильтр")
async def ask_delete_id(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        CreateFilter.entering_delete_id
    )

    await message.answer(
        "Введите ID фильтра:"
    )

@dp.message(CreateFilter.entering_delete_id)
async def delete_filter_handler(
    message: Message,
    state: FSMContext
):

    delete_filter(
        message.text,
        message.from_user.id
    )

    await message.answer(
        "✅ Фильтр удалён"
    )

    await state.clear()

@dp.message(CreateFilter.entering_search_query)
async def custom_search_query(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        category="search",
        search_query=message.text
    )

    await state.set_state(
        CreateFilter.choosing_condition
    )

    await message.answer(
        "Выберите состояние:",
        reply_markup=condition_keyboard()
    )

@dp.callback_query(F.data.startswith("cat_"))
async def choose_category(callback, state):

    category = callback.data.replace("cat_", "")

    if category == "search":

        await state.set_state(
            CreateFilter.entering_search_query
        )

        await callback.message.answer(
            "Введите поисковый запрос:"
        )

        return

    await state.update_data(
        category=category
    )

    await state.set_state(
        CreateFilter.choosing_condition
    )

    await callback.message.answer(
        "Выберите состояние:",
        reply_markup=condition_keyboard()
    )

@dp.message(F.text == "✅ Выбрать фильтр")
async def choose_active_filter(
    message: Message,
    state: FSMContext
):

    filters = get_filters(
        message.from_user.id
    )

    if not filters:
        await message.answer(
            "Фильтров нет"
        )
        return

    text = "Введите ID фильтра:\n\n"

    for item in filters:

        text += (
            f"ID: {item[0]}\n"
            f"Категория: {item[2]}\n\n"
        )

    await state.set_state(
        CreateFilter.choosing_active_filter
    )

    await message.answer(text)


@dp.message(
    CreateFilter.choosing_active_filter
)
async def save_active_filter(
    message: Message,
    state: FSMContext
):

    set_active_filter(
        int(message.text),
        message.from_user.id
    )

    await message.answer(
        f"✅ Фильтр {message.text} выбран"
    )

    await state.clear()

@dp.callback_query(F.data.startswith("cond_"))
async def choose_condition(
    callback: CallbackQuery,
    state: FSMContext
):

    condition = int(
        callback.data.replace("cond_", "")
    )

    await state.update_data(
        condition=condition
    )

    await state.set_state(
        CreateFilter.entering_min_price
    )

    await callback.message.answer(
        "Введите минимальную цену:"
    )


@dp.message(CreateFilter.entering_min_price)
async def min_price(message: Message, state: FSMContext):

    await state.update_data(
        min_price=int(message.text)
    )

    await state.set_state(
        CreateFilter.entering_max_price
    )

    await message.answer(
        "Введите максимальную цену:"
    )


@dp.message(CreateFilter.entering_max_price)
async def max_price(message: Message, state: FSMContext):

    data = await state.get_data()

    category = data["category"]
    min_price = data["min_price"]
    max_price = int(message.text)

    condition = data["condition"]

    add_filter(
        user_id=message.from_user.id,
        category=category,
        search_query=data.get("search_query"),
        condition=condition,
        min_price=min_price,
        max_price=max_price
    )

    await message.answer(
        "✅ Фильтр создан!"
    )

    await state.clear()


@dp.message(F.text == "📋 Мои фильтры")
async def my_filters(message: Message):

    filters = get_filters(message.from_user.id)

    if not filters:
        await message.answer(
            "Фильтров нет"
        )
        return

    text = "📋 Твои фильтры:\n\n"

    for item in filters:
        status = (
            "🟢 Активный"
            if item[7] == 1
            else "⚪ Неактивный"
        )

        text += (
            f"ID: {item[0]}\n"
            f"{status}\n"
            f"Категория: {item[2]}\n"
            f"Цена: {item[3]} - {item[4]}\n\n"
        )

    await message.answer(text)

async def monitor_filters():

    while True:

        try:

            filters = get_active_filters()

            for flt in filters:

                filter_id = flt[0]
                user_id = flt[1]
                category = flt[2]
                min_price = flt[3]
                max_price = flt[4]
                condition = flt[5]
                search_query = flt[6]

                items = await get_items(
                    category,
                    min_price,
                    max_price,
                    condition,
                    search_query
                )

                for item in items:

                    if is_seen(item["url"]):
                        continue

                    text = (
                        f"🆕 Новый товар\n\n"
                        f"📦 {item['title']}\n\n"
                        f"{item['url']}"
                    )

                    await bot.send_message(
                        user_id,
                        text
                    )

                    add_seen(item["url"])

        except Exception as e:
            print("MONITOR ERROR:", e)

        await asyncio.sleep(30)
async def main():

    asyncio.create_task(
        monitor_filters()
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())