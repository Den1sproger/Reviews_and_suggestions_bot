from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from ...bot_config import dp, bot, ADMIN
from .states import _ProfileStatesGroup
from database import (Database,
                      SQL_VIEW_REVIEWS,
                      SQL_VIEW_SUBSCRIBERS,
                      get_sql_add_to_moderated,
                      get_sql_add_suggestion_to_db,
                      get_sql_remove_published_review)
from ...keyboards import (check_review_ikb,
                          check_suggestion_ikb,
                          get_reviews_ikb)



review_text: str
suggestion_text: str
current_reviews_list = []
current_review_index: int


@dp.message_handler(Text(equals='Стоп'), state='*')
@dp.message_handler(Command('stop'), state='*')
async def stop(message: types.Message, state=FSMContext) -> None:
    if state is None: pass
    else:
        await state.finish()
        await message.reply('Вы прервали операцию')


@dp.message_handler(Text(equals='Посмотреть отзывы'))
@dp.message_handler(Command('view_reviews'))
async def view_rewievs(message: types.Message) -> None:
    global current_reviews_list, current_review_index
    current_reviews_list.clear()
    current_review_index = 0

    db = Database()

    current_reviews_list = db.get_list_of_full_data(SQL_VIEW_REVIEWS)

    if current_reviews_list:
        if message.chat.id != ADMIN:
            reply_markup = get_reviews_ikb(
                quantity_reviews=len(current_reviews_list),
                current_review_number=1
            )
        else:
            reply_markup = get_reviews_ikb(
                quantity_reviews=len(current_reviews_list),
                current_review_number=1, admin=True
            )
        await message.answer(
            text=current_reviews_list[0],
            reply_markup=reply_markup
        )
    else:
        await message.answer('Нет отзывов')


async def update_reviews_data(callback: types.CallbackQuery) -> None:
    if current_reviews_list:
        if callback.message.chat.id != ADMIN:
            reply_markup = get_reviews_ikb(
                quantity_reviews=len(current_reviews_list),
                current_review_number=current_review_index + 1
            )
        else:
            reply_markup = get_reviews_ikb(
                quantity_reviews=len(current_reviews_list),
                current_review_number=current_review_index + 1,
                admin=True
            )
        await callback.message.edit_text(current_reviews_list[current_review_index])
        await callback.message.edit_reply_markup(reply_markup=reply_markup)
    else:
        await callback.message.edit_text('Нет отзывов')


@dp.callback_query_handler(lambda callback: callback.data == 'previous_review')
async def previous_review(callback: types.CallbackQuery) -> None:
    global current_reviews_list, current_review_index
    current_review_index -= 1

    await update_reviews_data(callback)


@dp.callback_query_handler(lambda callback: callback.data == 'next_review')
async def next_review(callback: types.CallbackQuery) -> None:
    global current_reviews_list, current_review_index
    current_review_index += 1

    await update_reviews_data(callback)


@dp.message_handler(Text(equals='Написать отзыв'))
@dp.message_handler(Command('new_review'))
async def new_review(message: types.Message) -> None:
    db = Database()
    subscribers = db.get_list_of_full_data(SQL_VIEW_SUBSCRIBERS, users=True)

    if str(message.chat.id) in subscribers:
        await _ProfileStatesGroup.get_review.set()
        await message.answer(
            text='⚠️⚠️Важно: отзывы полностью анонимные⚠️⚠️\n' \
            'Напишите отзыв, пишите конструктивно, будьте вежливы в высказываниях'
        )
    else:
        await message.answer(
            text='⚠️⚠️⚠️Вы не можете оставлять отзывы, поскольку вы' \
                ' не являетесь подписчиком рассылки'
        )


@dp.message_handler(state=_ProfileStatesGroup.get_review)
async def get_review_text(message: types.Message) -> None:
    global review_text
    review_text = message.text

    await message.answer(
        text='Отправить отзыв?', reply_markup=check_review_ikb
    )


@dp.callback_query_handler(
        lambda callback: callback.data == 'send_review',
        state=_ProfileStatesGroup.get_review
)
async def send_review_to_moderation(callback: types.CallbackQuery,
                                    state=FSMContext) -> None:
    global review_text

    await state.finish()
    await callback.message.delete()

    db = Database()

    QUERY_TEXT = get_sql_add_to_moderated(review_text)
    db.action(QUERY_TEXT)
    review_text = ''

    MSG_TEXT = '✅Ваш отзыв отправлен на модерацию'
    await callback.answer(MSG_TEXT)
    await callback.message.answer(MSG_TEXT)
    await bot.send_message(
        chat_id=ADMIN, text='Поступил отзыв, проверьте модерацию'
    )


@dp.callback_query_handler(
        lambda callback: callback.data == 'rewrite_review',
        state=_ProfileStatesGroup.get_review
)
async def rewrite_review(callback: types.CallbackQuery) -> None:
    global review_text
    review_text = ''
    await callback.message.delete()
    await callback.message.answer('Напишите отзыв ещё раз')


@dp.message_handler(Text(equals='Написать предложение по улучшению работы'))
@dp.message_handler(Command('new_suggestion'))
async def new_suggestion(message: types.Message) -> None:
    await _ProfileStatesGroup.get_suggestion.set()
    await message.answer(
        text='Напишите предложение по улучшению работы системы' \
            ', пишите конструктивно, будьте вежливы в высказываниях'
    )


@dp.message_handler(state=_ProfileStatesGroup.get_suggestion)
async def get_review_text(message: types.Message) -> None:
    global suggestion_text
    suggestion_text = message.text

    await message.answer(
        text='Отправить предложение?', reply_markup=check_suggestion_ikb
    )


@dp.callback_query_handler(
        lambda callback: callback.data == 'send_suggestion',
        state=_ProfileStatesGroup.get_suggestion
)
async def add_suggestion_to_db(callback: types.CallbackQuery,
                               state=FSMContext) -> None:
    global suggestion_text

    await state.finish()
    await callback.message.delete()

    db = Database()

    QUERY_TEXT = get_sql_add_suggestion_to_db(suggestion_text)
    db.action(QUERY_TEXT)
    suggestion_text = ''

    MSG_TEXT = '✅Ваше предложение отправлено на модерацию'
    await callback.answer(MSG_TEXT)
    await callback.message.answer(MSG_TEXT)
    await bot.send_message(
        chat_id=ADMIN, text='Поступило предложение по улучшению, проверьте предложения'
    )


@dp.callback_query_handler(
        lambda callback: callback.data == 'rewrite_suggestion',
        state=_ProfileStatesGroup.get_suggestion
)
async def rewrite_suggestion(callback: types.CallbackQuery) -> None:
    global suggestion_text
    suggestion_text = ''
    await callback.message.delete()
    await callback.message.answer('Напишите ваше предложение ещё раз')


@dp.callback_query_handler(lambda callback: callback.data == 'remove_published_review')
async def remove_published_review(callback: types.CallbackQuery) -> None:
    global current_review_index, current_reviews_list
    current_review = current_reviews_list[current_review_index]
    last_length = len(current_reviews_list)
    current_reviews_list.pop(current_review_index)
    
    if current_review_index == last_length - 1 :
        current_review_index -= 1
    
    db = Database()

    REMOVE_QUERY_TEXT = get_sql_remove_published_review(current_review)
    db.action(REMOVE_QUERY_TEXT)

    await callback.answer('✅Отзыв удален')
    await update_reviews_data(callback)
