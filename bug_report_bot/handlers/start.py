"""
Основной файл с хэндлерами бота
"""


import os
import re
from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database.models import FSMBugReport, FSMPhone
from database.database import insert_bug_report, select_user_phone, insert_user_phone, select_bug_report, \
    insert_file_report, select_device_user
from keyboards import key_text
from keyboards.keyboards import start_keyboard, type_of_problem_keyboard, choices_file_keyboard
from loader import bot, logger
from settings import constants


async def start_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатвает команду /start
    :param message: Message
    :return: None
    """
    try:
        if message.from_user.username or select_user_phone(message.from_user.id) is not None:
            await bot.send_message(message.from_user.id, constants.WELCOME, reply_markup=start_keyboard())
        else:
            await bot.send_message(message.from_user.id, constants.WELCOME)
            await FSMPhone.phone.set()
            await bot.send_message(message.from_user.id, constants.PHONE_WARNING)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def phone_handler(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает введенный номер телефона пользователя
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        pattern = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
        if message.text.startswith('+7') and [message.text[2:]] == re.findall(pattern, message.text[2:]) \
                and len(message.text) >= 12:
            insert_user_phone((message.from_user.id, message.text))
            await state.finish()
            await bot.send_message(message.from_user.id, constants.PHONE_COMPLETE, reply_markup=start_keyboard())
        elif message.text.startswith('8') and [message.text[1:]] == re.findall(pattern, message.text[1:]) \
                and len(message.text) >= 11:
            insert_user_phone((message.from_user.id, message.text))
            await state.finish()
            await bot.send_message(message.from_user.id, constants.PHONE_COMPLETE, reply_markup=start_keyboard())
        elif [message.text] == re.findall(pattern, message.text) and len(message.text) >= 10:
            insert_user_phone((message.from_user.id, message.text))
            await state.finish()
            await bot.send_message(message.from_user.id, constants.PHONE_COMPLETE, reply_markup=start_keyboard())
        else:
            await bot.send_message(message.from_user.id, constants.INCORRECT_PHONE)
            await bot.send_message(message.from_user.id, constants.PHONE_WARNING)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def help_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатвает команду /help
    :param message: Message
    :return: None
    """
    try:
        await bot.send_message(message.from_user.id, constants.HELP)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def bug_report_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатвает команду /bug_report, входит в машину состояния
    :param message: Message
    :return: None
    """
    try:
        if not select_device_user(message.from_user.id):
            await FSMBugReport.device_model.set()
            await bot.send_message(message.from_user.id, constants.DEVICE_MODEL)
        else:
            await FSMBugReport.periodicity.set()
            await bot.send_message(message.from_user.id, constants.PERIODICITY)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def device_model_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние device_model
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            data['device_model'] = message.text
        await FSMBugReport.next()
        await bot.send_message(message.from_user.id, constants.PERIODICITY)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def periodicity_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние periodicity
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            data['periodicity'] = message.text
            device_model = select_device_user(message.from_user.id)
            if device_model:
                data['device_model'] = device_model
        await FSMBugReport.next()
        await bot.send_message(message.from_user.id, constants.TYPE_OF_PROBLEM, reply_markup=type_of_problem_keyboard())
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def type_of_problem_state(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние type_of_problem
    :param call: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            data['type_of_problem'] = call.data
        await FSMBugReport.next()
        await bot.send_message(call.from_user.id, constants.TITLE_MESSAGE)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def title_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние title
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            data['title'] = message.text
        await FSMBugReport.next()
        await bot.send_message(message.from_user.id, constants.DESCRIPTION)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def description_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние description
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMBugReport.next()
        await bot.send_message(message.from_user.id, constants.ADD_FILE, reply_markup=choices_file_keyboard())
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def choices_file_state(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние choices_file, в случае, если файлов нет, записывает репорт в БД
    :param call: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    try:
        if call.data == key_text.YES:
            if call.from_user.username is not None:
                username = call.from_user.username
            else:
                username = select_user_phone(call.from_user.id)
            async with state.proxy() as data:
                insert_bug_report((
                    call.from_user.id,
                    username,
                    data['device_model'],
                    data['periodicity'],
                    data['type_of_problem'],
                    data['title'],
                    datetime.today(),
                    data['description'],
                ))
            await state.finish()
            await bot.send_message(call.from_user.id, constants.REPORT_COMPLETE)
            await bot.send_message(call.from_user.id, constants.SEND_FILE)
        else:
            if call.from_user.username is not None:
                username = call.from_user.username
            else:
                username = select_user_phone(call.from_user.id)
            async with state.proxy() as data:
                insert_bug_report((
                    call.from_user.id,
                    username,
                    data['device_model'],
                    data['periodicity'],
                    data['type_of_problem'],
                    data['title'],
                    datetime.today(),
                    data['description'],
                ))
            await state.finish()
            await bot.send_message(call.from_user.id, constants.REPORT_COMPLETE)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def add_file_state(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает файлы и если они относятся к репорту, записываются в БД
    :param message: Message
    :return: None
    """
    try:
        report_tuple = select_bug_report(message.from_user.id)
        if report_tuple is not None:
            index = len(report_tuple) - 1
            if datetime.today().timestamp() - report_tuple[index][1].timestamp() <= 100:
                if message.document is not None:
                    file_id = message.document.file_id
                elif message.photo:
                    file_id = message.photo[len(message.photo) - 1].file_id
                elif message.video:
                    file_id = message.video.file_id
                file_path = (await bot.get_file(file_id)).file_path
                downloaded_file = await bot.download_file(file_path)
                # src = '/home/app/web/mediafiles/' + file_path
                src = os.path.abspath(os.path.join('../web/mediafiles/', file_path))
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file.read())
                insert_file_report((file_path, report_tuple[index][0]))
                await bot.send_message(message.from_user.id, constants.FILE_SAVE)
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
            await start_command(message)
        elif message.text == '/help' or message.text == key_text.HELP:
            await help_command(message)
        elif message.text == '/bug_report' or message.text == key_text.BUG_REPORT:
            await bug_report_command(message)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_start_handlers(dp: Dispatcher) -> None:
    """
    Функция - регистрирует все хэндлеры файла start.py
    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(phone_handler, content_types=['text'], state=FSMPhone.phone)
    dp.register_message_handler(cancel_state, Text(startswith=['/start', '/help', '/bug_report']), state='*')
    dp.register_message_handler(cancel_state, Text(startswith=[key_text.HELP, key_text.BUG_REPORT]), state='*')
    dp.register_message_handler(start_command, commands=['start'], state=None)
    dp.register_message_handler(help_command, commands=['help'], state=None)
    dp.register_message_handler(help_command, lambda message: message.text == key_text.HELP, state=None)
    dp.register_message_handler(bug_report_command, commands=['bug_report'], state=None)
    dp.register_message_handler(bug_report_command, lambda message: message.text == key_text.BUG_REPORT, state=None)
    dp.register_message_handler(device_model_state, content_types=['text'], state=FSMBugReport.device_model)
    dp.register_message_handler(periodicity_state, content_types=['text'], state=FSMBugReport.periodicity)
    dp.register_callback_query_handler(
        type_of_problem_state,
        lambda call: call.data in [key_text.CRASH, key_text.PERFOMANCE, key_text.INCORRECT_BEHAVIOR],
        state=FSMBugReport.type_of_problem
    )
    dp.register_message_handler(title_state, content_types=['text'], state=FSMBugReport.title)
    dp.register_message_handler(description_state, content_types=['text'], state=FSMBugReport.description)
    dp.register_callback_query_handler(choices_file_state, lambda call: call.data in [key_text.YES, key_text.NO],
                                       state=FSMBugReport.choices_file)
    dp.register_message_handler(add_file_state, content_types=['document', 'photo', 'video'], state=None)
