"""
Файл с хэндлерами старт/хэлп и регистрация
"""
import hashlib
import random
import re
from datetime import datetime
from typing import Tuple
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database.models import FSMSignUp
from database.database import select_zbt_user_phone, insert_zbt_user_phone, insert_zbt_profile, select_login, \
    select_user_profile
from handlers.admin import admin_command
from handlers.report import bug_report_command
from keyboards import key_text
from keyboards.keyboards import start_keyboard
from loader import bot, logger
from settings import constants


async def start_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатвает команду /start
    :param message: Message
    :return: None
    """
    try:
        await bot.send_message(message.from_user.id, constants.WELCOME, reply_markup=start_keyboard())
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def sign_up_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатвает команду /sign_up
    :param message: Message
    :return: None
    """
    try:
        if select_user_profile(message.from_user.id) is None:
            if message.from_user.username or select_zbt_user_phone(message.from_user.id) is not None:
                await FSMSignUp.email.set()
                await bot.send_message(message.from_user.id, constants.EMAIL)
            else:
                await FSMSignUp.phone.set()
                await bot.send_message(message.from_user.id, constants.PHONE_WARNING)
        else:
            await bot.send_message(message.from_user.id, constants.EXISTS_SIGN_UP)
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
            insert_zbt_user_phone((message.from_user.id, message.text))
            async with state.proxy() as data:
                data['username'] = message.text
            await FSMSignUp.next()
            await bot.send_message(message.from_user.id, constants.EMAIL)
        elif message.text.startswith('8') and [message.text[1:]] == re.findall(pattern, message.text[1:]) \
                and len(message.text) >= 11:
            insert_zbt_user_phone((message.from_user.id, message.text))
            async with state.proxy() as data:
                data['username'] = message.text
            await FSMSignUp.next()
            await bot.send_message(message.from_user.id, constants.EMAIL)
        elif [message.text] == re.findall(pattern, message.text) and len(message.text) >= 10:
            insert_zbt_user_phone((message.from_user.id, message.text))
            async with state.proxy() as data:
                data['username'] = message.text
            await FSMSignUp.next()
            await bot.send_message(message.from_user.id, constants.EMAIL)
        else:
            await bot.send_message(message.from_user.id, constants.INCORRECT_PHONE)
            await bot.send_message(message.from_user.id, constants.PHONE_WARNING)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def email_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает email пользователя.
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        if [message.text] == re.findall(r'\S+[@]\w+[.]\w+', message.text):
            async with state.proxy() as data:
                data['email'] = message.text
            await FSMSignUp.next()
            await bot.send_message(message.from_user.id, constants.DEVICE_MODEL)
        else:
            await bot.send_message(message.from_user.id, constants.INCORRECT_EMAIL)
            await bot.send_message(message.from_user.id, constants.EMAIL)
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
            if message.from_user.username:
                username = message.from_user.username
            else:
                username = data['username']
            login, password, hash_pass = generation_data()
            insert_zbt_profile((
                message.from_user.id, username, message.text,
                login, password, hash_pass,
                'Новый', datetime.today(), data['email']))
        await state.finish()
        await bot.send_message(message.from_user.id, constants.WAITING_INFO)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def generation_data() -> Tuple:
    """
    Функция - задаёт логику генерации логина и пароля
    """
    with open('en_words.txt', 'r', encoding='utf-8') as file:
        for elem in file:
            word_list = elem.split()
        password_data = list('abcdefghijklmnopqrstuvwxyz0123456789')
        flag = True
        login = ''
        while flag is True:
            for _ in range(2):
                login += random.choice(word_list)
            if select_login(login) is None:
                flag = False
        password = ''
        for _ in range(8):
            password += random.choice(password_data)
        hash_pass = hashlib.sha256(password.encode()).hexdigest()
        return login, password, hash_pass


async def help_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду /help
    :param message: Message
    :return: None
    """
    try:
        await bot.send_message(message.from_user.id, constants.HELP)
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
        elif message.text == '/sign_up' or message.text == key_text.SIGN_UP:
            await sign_up_command(message)
        elif message.text == '/bug_report' or message.text == key_text.BUG_REPORT:
            await bug_report_command(message)
        elif message.text == '/admin':
            await admin_command(message)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_start_handlers(dp: Dispatcher) -> None:
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
    dp.register_message_handler(start_command, commands=['start'], state=None)
    dp.register_message_handler(help_command, commands=['help'], state=None)
    dp.register_message_handler(phone_handler, content_types=['text'], state=FSMSignUp.phone)
    dp.register_message_handler(sign_up_command, commands=['sign_up'], state=None)
    dp.register_message_handler(sign_up_command, lambda message: message.text == key_text.SIGN_UP, state=None)
    dp.register_message_handler(help_command, lambda message: message.text == key_text.HELP, state=None)
    dp.register_message_handler(email_state, content_types=['text'], state=FSMSignUp.email)
    dp.register_message_handler(device_model_state, content_types=['text'], state=FSMSignUp.device_model)
