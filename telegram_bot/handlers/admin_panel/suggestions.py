from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from ...bot_config import dp, ADMIN
from ...keyboards import get_admin_suggestions_ikb
from database import (Database,
                      SQL_VIEW_SUGGESTIONS,
                      get_sql_remove_suggestion_from_db)


current_suggestions_list = []
current_suggestion_index: int



@dp.message_handler(Text(equals='Посмотреть предложения'), user_id=ADMIN)
@dp.message_handler(Command('view_suggestions'), user_id=ADMIN)
async def view_suggestions(message: types.Message) -> None:
    global current_suggestions_list, current_suggestion_index
    current_suggestion_index = 0

    db = Database()
    current_suggestions_list = db.get_list_of_full_data(SQL_VIEW_SUGGESTIONS)

    if current_suggestions_list:
        await message.answer(
            text=current_suggestions_list[0],
            reply_markup=get_admin_suggestions_ikb(
                quantity_suggestions=len(current_suggestions_list),
                current_suggestion_number=1
            )
        )
    else:
        await message.answer('Нет предложений')


async def update_suggest_data(callback: types.CallbackQuery) -> None:
    if current_suggestions_list:
        await callback.message.edit_text(current_suggestions_list[current_suggestion_index])
        await callback.message.edit_reply_markup(
            reply_markup=get_admin_suggestions_ikb(
                quantity_suggestions=len(current_suggestions_list),
                current_suggestion_number=current_suggestion_index + 1
            )
        )
    else:
        await callback.message.edit_text('Нет предложений')


@dp.callback_query_handler(lambda callback: callback.data == 'previous_suggestion')
async def previous_suggestion(callback: types.CallbackQuery) -> None:
    global current_suggestions_list, current_suggestion_index
    current_suggestion_index -= 1

    await update_suggest_data(callback)


@dp.callback_query_handler(lambda callback: callback.data == 'next_suggestion')
async def next_suggestion(callback: types.CallbackQuery) -> None:
    global current_suggestions_list, current_suggestion_index
    current_suggestion_index += 1

    await update_suggest_data(callback)


@dp.callback_query_handler(lambda callback: callback.data == 'remove_suggestion')
async def delete_suggestion(callback: types.CallbackQuery) -> None:
    global current_suggestions_list, current_suggestion_index
    current_review = current_suggestions_list[current_suggestion_index]
    last_length = len(current_suggestions_list)
    current_suggestions_list.pop(current_suggestion_index)
    
    if current_suggestion_index == last_length - 1 :
        current_suggestion_index -= 1
    
    db = Database()

    REMOVE_QUERY_TEXT = get_sql_remove_suggestion_from_db(current_review)
    db.action(REMOVE_QUERY_TEXT)

    await callback.answer('✅Предложение удалено')
    await update_suggest_data(callback)



