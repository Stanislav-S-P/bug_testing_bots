"""
Файл с хэндлерами действий администратора
"""
import random
import time
import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database.database import select_admin, select_all_user, update_status_command, delete_zbt_profile, \
    update_status_profile, select_register_data_profile, select_all_new_status, select_ip_address
from database.models import FSMAdminMessage, FSMQuantity
from handlers import report
from handlers import start
from keyboards import key_text
from keyboards.keyboards import admin_menu
from loader import logger, bot
from settings import constants


async def admin_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду /admin
    :param message: Message
    :return: None
    """
    try:
        if select_admin(message.from_user.id):
            await bot.send_message(message.from_user.id, constants.ADMIN, reply_markup=admin_menu())
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def send_admin_message(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает подкоманду отправки сообщения. Входит в машину состояния.
    :param message: Message
    :return: None
    """
    try:
        if select_admin(message.from_user.id):
            await FSMAdminMessage.admin_message.set()
            await bot.send_message(message.from_user.id, constants.ADMIN_MESSAGE)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def admin_message_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние admin_message.
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        if select_admin(message.from_user.id):
            await state.finish()
            users = select_all_user()
            if users:
                for elem in users:
                    print(elem)
                    await bot.send_message(elem[0], message.text)
                    time.sleep(0.3)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def admin_open_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает подкоманду открыть ЗБТ. Входит в машину стостояния
    :param message: Message
    :return: None
    """
    try:
        await FSMQuantity.quantity.set()
        await bot.send_message(message.from_user.id, constants.QUANTITY)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def quantity_user_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние quantity. Открывает пользователям доступ к сценарию ЗБТ.
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        if message.text.isdigit():
            await state.finish()
            update_status_command('Открыта', '/bug_report')
            users = select_all_new_status()
            if users:
                random.shuffle(users)
                if len(users) > int(message.text):
                    for index in range(int(message.text)):
                        update_status_profile(users[index][0])
                else:
                    for index in range(len(users)):
                        update_status_profile(users[index][0])
            active_users = select_register_data_profile()
            if active_users:
                ip_address = select_ip_address()
                for elem in active_users:
                    await bot.send_message(elem[0], constants.LOGIN.format(elem[2], elem[3]), parse_mode='Markdown')
                    request_dict = {'nickname': elem[1], 'email': elem[2], 'password': elem[4]}
                    requests.post(f'http://{ip_address}/api/registration', json=request_dict)
                    time.sleep(0.3)
        else:
            await bot.send_message(message.from_user.id, constants.INCORRECT_QUANTITY)
            await bot.send_message(message.from_user.id, constants.QUANTITY)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def admin_close_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает подкоманду закрыть ЗБТ. Закрывает доступ к сценарию ЗБТ.
    :param message: Message
    :return: None
    """
    try:
        if select_admin(message.from_user.id):
            update_status_command('Закрыта', '/bug_report')
            delete_zbt_profile()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def cancel_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - реагирует на команды и выводит из машины состояния пользователя
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
        if message.text == '/start':
            await start.start_command(message)
        elif message.text == '/help' or message.text == key_text.HELP:
            await start.help_command(message)
        elif message.text == '/sign_up' or message.text == key_text.SIGN_UP:
            await start.sign_up_command(message)
        elif message.text == '/bug_report' or message.text == key_text.BUG_REPORT:
            await report.bug_report_command(message)
        elif message.text == '/admin':
            await admin_command(message)
        elif message.text == key_text.SEND_MESSAGE:
            await send_admin_message(message)
        elif message.text == key_text.OPEN_ZBT:
            await admin_open_command(message)
        elif message.text == key_text.CLOSE_ZBT:
            await admin_close_command(message)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_admin_handlers(dp: Dispatcher) -> None:
    """
    Функция - регистрирует все хэндлеры файла admin.py
    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(
        cancel_state, Text(startswith=['/start', '/help', '/sign_up', '/bug_report', '/admin']), state='*'
    )
    dp.register_message_handler(
        cancel_state, Text(startswith=[key_text.HELP, key_text.BUG_REPORT, key_text.SIGN_UP,
                                       key_text.SEND_MESSAGE, key_text.OPEN_ZBT, key_text.CLOSE_ZBT]), state='*'
    )
    dp.register_message_handler(admin_command, lambda message: message.text == '/admin', state=None)
    dp.register_message_handler(send_admin_message, lambda message: message.text == key_text.SEND_MESSAGE, state=None)
    dp.register_message_handler(admin_message_state, content_types=['text'], state=FSMAdminMessage.admin_message)
    dp.register_message_handler(admin_open_command, lambda message: message.text == key_text.OPEN_ZBT, state=None)
    dp.register_message_handler(quantity_user_state, content_types=['text'], state=FSMQuantity.quantity)
    dp.register_message_handler(admin_close_command, lambda message: message.text == key_text.CLOSE_ZBT, state=None)
