from aiogram.types import CallbackQuery
from jinja2 import Template
from aiogram.utils.exceptions import BadRequest

from handlers.markups import faq_markup, back_faq_menu
from loader import dp, bot


@dp.callback_query_handler(text='back', state='*')
@dp.callback_query_handler(text='back_to_faq', state='*')
@dp.callback_query_handler(text='quick_start', state='*')
async def show_menu(call: CallbackQuery) -> None:
    template = Template(open('handlers/templates/instructions.html').read())
    try:
        await call.message.edit_text(text=template.render(),
                                     parse_mode='HTML',
                                     reply_markup=faq_markup())
    except BadRequest:
        await call.message.delete()
        await call.message.answer(text=template.render(),
                                  parse_mode='HTML',
                                  reply_markup=faq_markup())


@dp.callback_query_handler(text='faq_show_task', state='*')
async def show_task(call: CallbackQuery) -> None:
    photo = open('./static/images/example_task.png', 'rb')
    template = Template(open('handlers/templates/faq/show_task.html').read())
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo=photo,
                         caption=template.render(),
                         parse_mode='HTML',
                         reply_markup=back_faq_menu())


@dp.callback_query_handler(text='faq_criteria', state='*')
async def criteria(call: CallbackQuery) -> None:
    template = Template(open('handlers/templates/faq/criteria.html').read())
    await call.message.edit_text(text=template.render(),
                                 parse_mode='HTML',
                                 reply_markup=back_faq_menu())
