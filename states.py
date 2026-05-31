from aiogram.fsm.state import State, StatesGroup


class CreateFilter(StatesGroup):
    choosing_category = State()

    entering_search_query = State()

    choosing_condition = State()
    entering_min_price = State()
    entering_max_price = State()
    entering_delete_id = State()
    choosing_active_filter = State()