from aiogram.types import BotCommand


set_default_commands = [
    BotCommand('start', 'запустить бота'),
    BotCommand('help', 'помощь'),
    BotCommand('view_reviews', 'посмотреть отзывы'),
    BotCommand('new_review', 'добавить отзыв'),
    BotCommand('new_suggestion', 'написать предложение по улучшению работы'),
    BotCommand('stop', 'прервать операцию')
]

set_admin_commands = [
    BotCommand('start', 'запустить бота'),
    BotCommand('help', 'помощь'),
    BotCommand('view_reviews', 'посмотреть отзывы'),
    BotCommand('view_moderating', 'посмотреть список отзывов на модерации'),
    BotCommand('view_suggestions', 'посмотреть предложения'),
    BotCommand('new_review', 'добавить отзыв'),
    BotCommand('new_suggestion', 'написать предложение по улучшению работы'),
    BotCommand('stop', 'прервать операцию')
]