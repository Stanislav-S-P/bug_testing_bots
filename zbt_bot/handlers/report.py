"""
Файл с хэндлерами заполнения репорта
"""


import os
from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database.database import select_zbt_bug_report, insert_zbt_file_report, insert_zbt_bug_report, \
    select_data_profile, select_command, select_status_profile
from database.models import FSMBugReport
from handlers import admin
from handlers import start
from keyboards import key_text
from keyboards.keyboards import type_of_problem_keyboard, choices_file_keyboard
from loader import logger, bot
from settings import constants


async def bug_report_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатвает команду /bug_report, входит в машину состояния
    :param message: Message
    :return: None
    """
    try:
        if select_command('/bug_report') == 'Открыта' and select_status_profile(message.from_user.id) == 'Активный':
            await FSMBugReport.type_of_problem.set()
            await bot.send_message(
                message.from_user.id, constants.TYPE_OF_PROBLEM, reply_markup=type_of_problem_keyboard()
            )
        else:
            await bot.send_message(message.from_user.id, constants.NO_STARTING)
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
        await bot.send_message(call.from_user.id, constants.PERIODICITY)
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
            device_model = select_data_profile(message.from_user.id)
            data['username'] = device_model[0][0]
            data['device_model'] = device_model[0][1]
        await FSMBugReport.next()
        await bot.send_message(message.from_user.id, constants.TITLE_MESSAGE)
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
            async with state.proxy() as data:
                insert_zbt_bug_report((
                    call.from_user.id,
                    data['username'],
                    data['device_model'],
                    data['periodicity'],
                    data['type_of_problem'],
                    data['title'],
                    data['description'],
                    datetime.today(),
                ))
            await state.finish()
            await bot.send_message(call.from_user.id, constants.REPORT_COMPLETE)
            await bot.send_message(call.from_user.id, constants.SEND_FILE)
        else:
            async with state.proxy() as data:
                insert_zbt_bug_report((
                    call.from_user.id,
                    data['username'],
                    data['device_model'],
                    data['periodicity'],
                    data['type_of_problem'],
                    data['title'],
                    data['description'],
                    datetime.today(),
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
        report_tuple = select_zbt_bug_report(message.from_user.id)
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
                src = os.path.abspath(os.path.join('../web/mediafiles/', file_path))
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file.read())
                insert_zbt_file_report((file_path, report_tuple[index][0]))
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
            await start.start_command(message)
        elif message.text == '/help' or message.text == key_text.HELP:
            await start.help_command(message)
        elif message.text == '/bug_report' or message.text == key_text.BUG_REPORT:
            await bug_report_command(message)
        elif message.text == '/admin':
            await admin.admin_command(message)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_report_handlers(dp: Dispatcher) -> None:
    """
    Функция - регистрирует все хэндлеры файла start.py
    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(
        cancel_state, Text(startswith=['/start', '/help', '/sign_up', '/bug_report', '/admin']), state='*'
    )
    dp.register_message_handler(
        cancel_state, Text(startswith=[key_text.HELP, key_text.BUG_REPORT, key_text.SIGN_UP]), state='*'
    )
    dp.register_message_handler(bug_report_command, commands=['bug_report'], state=None)
    dp.register_message_handler(bug_report_command, lambda message: message.text == key_text.BUG_REPORT, state=None)
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
