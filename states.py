from aiogram.dispatcher.filters.state import State, StatesGroup

class AddBanwordsList(StatesGroup):
    Text = State()

class DelBanword(StatesGroup):
    Text = State()

class AddChat(StatesGroup):
    Text = State()

class DelChat(StatesGroup):
    Text = State()