from aiogram.dispatcher.filters.state import State, StatesGroup



class _ProfileStatesGroup(StatesGroup):
    get_review = State()
    get_suggestion = State()