"""
Файл с моделями машины состояний
"""


from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMBugReport(StatesGroup):
    device_model = State()
    periodicity = State()
    type_of_problem = State()
    title = State()
    description = State()
    choices_file = State()


class FSMPhone(StatesGroup):
    phone = State()
