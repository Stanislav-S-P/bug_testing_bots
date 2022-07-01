"""
Файл - содержит клавиатуры бота
"""


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import key_text


def start_keyboard() -> ReplyKeyboardMarkup:
    """
    Функция - создаёт и возвращает клавиатуру главного меню бота
    :return: ReplyKeyboardMarkup
    """
    keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    first_key = KeyboardButton(text=key_text.BUG_REPORT)
    second_key = KeyboardButton(text=key_text.HELP)
    return keyboards.add(first_key, second_key)


def type_of_problem_keyboard() -> InlineKeyboardMarkup:
    """
    Функция - создаёт и возвращает клавиатуру выбора типа проблемы
    :return: InlineKeyboardMarkup
    """
    keyboards = InlineKeyboardMarkup(row_width=2)
    first_key = InlineKeyboardButton(text=key_text.CRASH, callback_data=key_text.CRASH)
    second_key = InlineKeyboardButton(text=key_text.PERFOMANCE, callback_data=key_text.PERFOMANCE)
    third_key = InlineKeyboardButton(text=key_text.INCORRECT_BEHAVIOR, callback_data=key_text.INCORRECT_BEHAVIOR)
    return keyboards.add(first_key, second_key, third_key)


def choices_file_keyboard() -> InlineKeyboardMarkup:
    """
    Функция - создаёт и возвращает клавиатуру опроса о добавлении файлов
    :return: InlineKeyboardMarkup
    """
    keyboards = InlineKeyboardMarkup(row_width=2)
    first_key = InlineKeyboardButton(text=key_text.YES, callback_data=key_text.YES)
    second_key = InlineKeyboardButton(text=key_text.NO, callback_data=key_text.NO)
    return keyboards.add(first_key, second_key)
