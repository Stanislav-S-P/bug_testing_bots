"""
Файл содержащий Token бота и данные для подключения к БД
"""

import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Файл .env отсутствует')
else:
    load_dotenv()


"""Токен бота"""
TOKEN = os.environ.get('TOKEN')


"""Данные БД"""
HOST = os.environ.get('HOST')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
PORT = os.environ.get('PORT')
