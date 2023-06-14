from aiogram import executor
from telegram_bot import dp
from telegram_bot.handlers.general.start import *
from telegram_bot.handlers.general.default_commands import *
from telegram_bot.handlers.admin_panel.reviews import *
from telegram_bot.handlers.admin_panel.suggestions import *



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)