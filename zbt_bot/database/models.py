"""
Файл с моделями машины состояний
"""


from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMBugReport(StatesGroup):
    type_of_problem = State()
    periodicity = State()
    title = State()
    description = State()
    choices_file = State()


class FSMSignUp(StatesGroup):
    phone = State()
    email = State()
    device_model = State()


class FSMAdminMessage(StatesGroup):
    admin_message = State()


class FSMQuantity(StatesGroup):
    quantity = State()
