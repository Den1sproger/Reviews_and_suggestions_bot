import logging

from aiogram import executor
from telegram_bot import dp
from telegram_bot.handlers.common.start import *
from telegram_bot.handlers.common.default_commands import *
from telegram_bot.handlers.admin_panel.reviews import *
from telegram_bot.handlers.admin_panel.suggestions import *


LOG_FILENAME = "/home/reviews_suggestions/py_log.log"
logging.basicConfig(level=logging.INFO, filename=LOG_FILENAME, filemode="w")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)