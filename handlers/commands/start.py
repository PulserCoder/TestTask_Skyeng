from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message
from jinja2 import Template

from handlers.markups import quick_start_markup
from loader import dp
from implemented import user_service

@dp.message_handler(CommandStart(), state='*')
async def start(message: Message) -> None:
    try:
        user_service.create({"userid": message.chat.id,
                             "username": message.chat.username,
                             "first_name": message.chat.first_name,
                             "last_name": message.chat.last_name})
    except Exception:
        pass
    template = Template(open('handlers/templates/start.html').read())
    await message.answer(template.render(message=message), reply_markup=quick_start_markup(),
                         parse_mode='HTML')
