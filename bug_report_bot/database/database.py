"""
Файл с запросами к базе данных
"""


from sqlite3 import Cursor
import psycopg2
from typing import Tuple, Callable, Any, List
from loader import logger
from settings.settings import HOST, USER, PASSWORD, DB_NAME, PORT


def db_decorator(func: Callable) -> Any:
    """
    Декоратор - Подключается к базе данных
    :param func: Callable
    :return: Any
    """
    def wrapped_func(*args, **kwargs):
        try:
            connection = psycopg2.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DB_NAME,
                port=PORT
            )
            connection.autocommit = True
            with connection.cursor() as cursor:
                result = func(*args, **kwargs, cursor=cursor)
                return result
        except Exception as ex:
            logger.error('Ошибка БД', exc_info=ex)
            print(ex, 'Ошибка БД')
        finally:
            connection.close()
    return wrapped_func


@db_decorator
def insert_bug_report(tuple_report: Tuple, cursor: Cursor) -> None:
    """
    Функция - совершает сохранение данных в таблицу bug_report
    :param tuple_report: Tuple
    :param cursor: Cursor
    :return: None
    """
    cursor.execute(
        """INSERT INTO bug_report 
        ("user_id", "username", "device_model", "periodicity", 
        "type_of_problem", "title", "created_at", "description") 
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s);""", tuple_report
    )


@db_decorator
def select_bug_report(user_id: int, cursor: Cursor) -> List:
    """
    Функция - запрашивает  данные из таблицы bug_report
    :param user_id: int
    :param cursor: Cursor
    :return: List
    """
    cursor.execute("""SELECT id, created_at FROM bug_report WHERE user_id=%s;""", (user_id, ))
    result = cursor.fetchall()
    return result


@db_decorator
def select_device_user(user_id: int, cursor: Cursor) -> List:
    """
    Функция - запрашивает  данные из таблицы bug_report
    :param user_id: int
    :param cursor: Cursor
    :return: Union[str, None]
    """
    cursor.execute("""SELECT device_model FROM bug_report WHERE user_id=%s;""", (user_id, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def select_user_phone(user_id: int, cursor: Cursor) -> str:
    """
    Функция - запрашивает с таблицы user_phone, номер телефона пользователя
    :param user_id: int
    :param cursor: Cursor
    :return: str
    """
    cursor.execute("""SELECT phone FROM user_phone WHERE user_id=%s""", (user_id, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def insert_user_phone(user_tuple: Tuple, cursor: Cursor) -> None:
    """
    Функция - совершает сохранение данных в таблицу user_phone
    :param user_tuple: Tuple
    :param cursor: Cursor
    :return: None
    """
    cursor.execute("""INSERT INTO user_phone ("user_id", "phone") VALUES ( %s, %s)""", user_tuple)


@db_decorator
def insert_file_report(user_tuple: Tuple, cursor: Cursor) -> None:
    """
    Функция - совершает сохранение данных в таблицу file_report
    :param user_tuple: Tuple
    :param cursor: Cursor
    :return: None
    """
    cursor.execute("""INSERT INTO file_report ("file", "report_id") VALUES ( %s, %s)""", user_tuple)
