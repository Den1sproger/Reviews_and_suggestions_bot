from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types.bot_command_scope import BotCommandScopeDefault, BotCommandScopeChat
from ...bot_config import dp, ADMIN, bot
from ...commands.set_bot_commands import set_default_commands, set_admin_commands
from ...keyboards import general_menu_kb, get_admin_menu_kb



WELCOME_TEXT = """
Привет👋👋👋
Я бот отзывов и предложений📋📋📋
"""

ADMIN_HELP_TEXT = """
❗️❗️❗️<b>Вы являетесь администратором системы</b>❗️❗️❗️
👨🏻‍⚕️👨🏻‍⚕️👨🏻‍⚕️
/start - запуск бота
/help - помощь
/view_reviews - просмотреть отзывы
/view_moderating - посмотреть отзывы на модерации
/view_suggestions - посмотреть предложения по улучшению
/new_review - добавить отзыв
/new_suggestion - написать предложение по улучшению работы
/stop - прервать операцию
"""

USER_HELP_TEXT = """
/start - запуск бота
/help - помощь
/view_reviews - просмотреть отзывы
/new_review - добавить отзыв
/new_suggestion - написать предложение по улучшению работы
/stop - прервать операцию
"""


@dp.message_handler(Command('start'))
async def start(message: types.Message) -> None:
    if message.chat.id != ADMIN:
        await message.answer(WELCOME_TEXT, reply_markup=general_menu_kb)
        await bot.set_my_commands(
            set_default_commands, scope=BotCommandScopeDefault() 
        )
    else:
        await message.answer(WELCOME_TEXT, reply_markup=get_admin_menu_kb())
        await bot.set_my_commands(
            set_admin_commands, scope=BotCommandScopeChat(chat_id=ADMIN)
        )


@dp.message_handler(Command('help'))
async def send_instruction(message: types.Message) -> None:
    if message.chat.id != ADMIN:
        await message.answer(USER_HELP_TEXT)
    else:
        await message.answer(ADMIN_HELP_TEXT, parse_mode='HTML')