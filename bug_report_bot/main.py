"""Файл для запуска бота. Содержит в себе все регистраторы приложения"""


from loader import dp
from aiogram.utils import executor
from handlers import start, echo


start.register_start_handlers(dp)
echo.register_echo_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
