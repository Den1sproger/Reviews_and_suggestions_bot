from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from ...bot_config import dp, ADMIN
from ...keyboards import get_admin_moderation_ikb
from database import (Database,
                      SQL_VIEW_MODERATING,
                      get_sql_add_review_to_db,
                      get_sql_remove_from_moderated)



current_modder_list = []
current_modder_index: int


@dp.message_handler(Text(equals='Посмотреть список отзывов на модерации'), user_id=ADMIN)
@dp.message_handler(Command('view_moderating'), user_id=ADMIN)
async def view_moderating(message: types.Message) -> None:
    global current_modder_list, current_modder_index
    current_modder_index = 0
    db = Database()

    current_modder_list = db.get_list_of_full_data(SQL_VIEW_MODERATING)

    if current_modder_list:
        await message.answer(
            text=current_modder_list[0],
            reply_markup=get_admin_moderation_ikb(
                quantity_reviews=len(current_modder_list),
                current_review_number=1
            )
        )
    else:
        await message.answer('Нет отзывов на модерации')


async def update_modder_data(callback: types.CallbackQuery) -> None:
    if current_modder_list:
        await callback.message.edit_text(current_modder_list[current_modder_index])
        await callback.message.edit_reply_markup(
            reply_markup=get_admin_moderation_ikb(
                quantity_reviews=len(current_modder_list),
                current_review_number=current_modder_index + 1
            )
        )
    else:
        await callback.message.edit_text('Нет отзывов на модерации')


@dp.callback_query_handler(lambda callback: callback.data == 'previous_modder')
async def previous_modder(callback: types.CallbackQuery) -> None:
    global current_modder_list, current_modder_index
    current_modder_index -= 1

    await update_modder_data(callback)


@dp.callback_query_handler(lambda callback: callback.data == 'next_modder')
async def next_modder(callback: types.CallbackQuery) -> None:
    global current_modder_list, current_modder_index
    current_modder_index += 1

    await update_modder_data(callback)


@dp.callback_query_handler(lambda callback: callback.data == 'publish_review')
async def publish_review(callback: types.CallbackQuery) -> None:
    global current_modder_list, current_modder_index
    current_review = current_modder_list[current_modder_index]
    last_length = len(current_modder_list)
    current_modder_list.pop(current_modder_index)
    
    if current_modder_index == last_length - 1 :
        current_modder_index -= 1
    
    db = Database()

    REMOVE_QUERY_TEXT = get_sql_remove_from_moderated(current_review)
    db.action(REMOVE_QUERY_TEXT)

    ADD_QUERY_TEXT = get_sql_add_review_to_db(current_review)
    db.action(ADD_QUERY_TEXT)

    await callback.answer('✅Отзыв добавлен')
    await update_modder_data(callback)


@dp.callback_query_handler(lambda callback: callback.data == 'delete_review')
async def delete_review(callback: types.CallbackQuery) -> None:
    global current_modder_list, current_modder_index
    current_review = current_modder_list[current_modder_index]
    last_length = len(current_modder_list)
    current_modder_list.pop(current_modder_index)
    
    if current_modder_index == last_length - 1 :
        current_modder_index -= 1
    
    db = Database()

    REMOVE_QUERY_TEXT = get_sql_remove_from_moderated(current_review)
    db.action(REMOVE_QUERY_TEXT)

    await callback.answer('✅Отзыв удален')
    await update_modder_data(callback)
