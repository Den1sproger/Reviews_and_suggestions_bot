from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton



check_review_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Отправить', callback_data='send_review'),
            InlineKeyboardButton('Переписать', callback_data='rewrite_review')
        ]
    ]
)

check_suggestion_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Отправить', callback_data='send_suggestion'),
            InlineKeyboardButton('Переписать', callback_data='rewrite_suggestion')
        ]
    ]
)


general_menu_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton('Посмотреть отзывы')],
        [KeyboardButton('Написать отзыв')],
        [KeyboardButton('Написать предложение по улучшению работы')],
        [KeyboardButton('Стоп')]
    ]
)

def get_admin_menu_kb() -> ReplyKeyboardMarkup:
    admin_menu_kb = general_menu_kb
    admin_menu_kb.add('Посмотреть список отзывов на модерации')
    admin_menu_kb.add('Посмотреть предложения')
    return admin_menu_kb