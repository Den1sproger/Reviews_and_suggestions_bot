from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def get_reviews_ikb(quantity_reviews: int,
                    current_review_number: int,
                    admin: bool = False) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton('<', callback_data='previous_review'),
            InlineKeyboardButton(f'{current_review_number}/{quantity_reviews}', callback_data='current_review'),
            InlineKeyboardButton('>', callback_data='next_review')
        ]
    ]
    if not admin:
        pass
    else:
        inline_keyboard.append(
            [InlineKeyboardButton('Удалить', callback_data='remove_published_review')]
        )

    if current_review_number == 1:
        inline_keyboard[0].pop(0)
    elif current_review_number == quantity_reviews:
        inline_keyboard[0].pop(-1)

    ikb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return ikb


def get_admin_moderation_ikb(quantity_reviews: int,
                             current_review_number: int) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton('<', callback_data='previous_modder'),
            InlineKeyboardButton(f'{current_review_number}/{quantity_reviews}', callback_data='current_review'),
            InlineKeyboardButton('>', callback_data='next_modder')
        ],
        [
            InlineKeyboardButton('Опубликовать', callback_data='publish_review'),
            InlineKeyboardButton('Не опубликовывать', callback_data='delete_review')
        ]
    ]

    if current_review_number == 1:
        inline_keyboard[0].pop(0)
    elif current_review_number == quantity_reviews:
        inline_keyboard[0].pop(-1)

    ikb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return ikb


def get_admin_suggestions_ikb(quantity_suggestions: int,
                              current_suggestion_number: int) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton('<', callback_data='previous_suggestion'),
            InlineKeyboardButton(f'{current_suggestion_number}/{quantity_suggestions}', callback_data='current_suggestion'),
            InlineKeyboardButton('>', callback_data='next_suggestion')
        ],
        [
            InlineKeyboardButton('Удалить', callback_data='remove_suggestion')
        ]
    ]

    if current_suggestion_number == 1:
        inline_keyboard[0].pop(0)
    elif current_suggestion_number == quantity_suggestions:
        inline_keyboard[0].pop(-1)

    ikb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return ikb