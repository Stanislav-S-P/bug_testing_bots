"""
Файл с запросами к базе данных
"""


from sqlite3 import Cursor
import psycopg2
from typing import Tuple, Callable, Any, List, Union
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
        finally:
            connection.close()
    return wrapped_func


"""Запросы к таблице zbt_profile"""


@db_decorator
def insert_zbt_profile(tuple_profile: Tuple, cursor: Cursor) -> None:
    cursor.execute(
        """INSERT INTO zbt_profile 
        ("user_id", "username", "device_model", "login", 
        "password", "hash_password", "status", "created_at", "email")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", tuple_profile
    )


@db_decorator
def delete_zbt_profile(cursor: Cursor) -> None:
    cursor.execute("""DELETE FROM zbt_profile WHERE status='Активный'""")


@db_decorator
def select_login(login: str, cursor: Cursor) -> Union[None, str]:
    cursor.execute("""SELECT login FROM zbt_profile WHERE login=%s""", (login, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def select_user_profile(user_id: int, cursor: Cursor) -> Union[None, int]:
    cursor.execute("""SELECT user_id FROM zbt_profile WHERE user_id=%s""", (user_id, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def select_all_user(cursor: Cursor) -> List:
    cursor.execute("""SELECT user_id FROM zbt_profile WHERE status!='Заблокирован'""")
    result = cursor.fetchall()
    return result


@db_decorator
def select_all_new_status(cursor: Cursor) -> List:
    cursor.execute("""SELECT user_id FROM zbt_profile WHERE status='Новый'""")
    result = cursor.fetchall()
    return result


@db_decorator
def select_data_profile(user_id: int, cursor: Cursor) -> List:
    cursor.execute("""SELECT username, device_model FROM zbt_profile WHERE user_id=%s""", (user_id, ))
    result = cursor.fetchall()
    return result


@db_decorator
def select_status_profile(user_id: int, cursor: Cursor) -> List:
    cursor.execute("""SELECT status FROM zbt_profile WHERE user_id=%s""", (user_id, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def update_status_profile(user_id: int, cursor: Cursor) -> None:
    cursor.execute("""UPDATE zbt_profile SET status='Активный' WHERE user_id=%s""", (user_id, ))


@db_decorator
def select_register_data_profile(cursor: Cursor) -> List:
    cursor.execute("""SELECT user_id, login, email, password, hash_password FROM zbt_profile WHERE status='Активный'""")
    result = cursor.fetchall()
    return result


"""Запросы к таблице zbt_bug_report"""


@db_decorator
def insert_zbt_bug_report(tuple_report: Tuple, cursor: Cursor) -> None:
    cursor.execute(
        """INSERT INTO zbt_bug_report 
        ("user_id", "username", "device_model", "periodicity", 
        "type_of_problem", "title", "description", "created_at") 
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s);""", tuple_report
    )


@db_decorator
def select_zbt_bug_report(user_id: int, cursor: Cursor) -> List:
    cursor.execute("""SELECT id, created_at FROM zbt_bug_report WHERE user_id=%s;""", (user_id, ))
    result = cursor.fetchall()
    return result


"""Запросы к таблице zbt_user_phone"""


@db_decorator
def select_zbt_user_phone(user_id: int, cursor: Cursor) -> str:
    cursor.execute("""SELECT phone FROM zbt_user_phone WHERE user_id=%s""", (user_id, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def insert_zbt_user_phone(user_tuple: Tuple, cursor: Cursor) -> None:
    cursor.execute("""INSERT INTO zbt_user_phone ("user_id", "phone") VALUES ( %s, %s)""", user_tuple)


"""Запросы к таблице zbt_file_report"""


@db_decorator
def insert_zbt_file_report(user_tuple: Tuple, cursor: Cursor) -> None:
    cursor.execute("""INSERT INTO zbt_file_report ("file", "report_id") VALUES ( %s, %s)""", user_tuple)


"""Запросы к таблице zbt_command"""


@db_decorator
def select_command(command: str, cursor: Cursor) -> str:
    cursor.execute("""SELECT status FROM zbt_command WHERE command=%s""", (command, ))
    result, *_ = cursor.fetchone()
    return result


@db_decorator
def update_status_command(status: str, command: str, cursor: Cursor) -> None:
    cursor.execute("""UPDATE zbt_command SET status=%s WHERE command=%s""", (status, command))


"""Запросы к таблице zbt_admin"""


@db_decorator
def select_admin(user_id: int, cursor: Cursor) -> List:
    cursor.execute("""SELECT user_id FROM zbt_admin WHERE user_id=%s""", (user_id, ))
    result, *_ = cursor.fetchone()
    return result


"""Запросы к таблице zbt_ip_address"""


@db_decorator
def select_ip_address(cursor: Cursor) -> List:
    cursor.execute("""SELECT ip_address FROM zbt_ip_address""")
    result, *_ = cursor.fetchone()
    return result
