from typing import List

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from jinja2 import Template

from loader import dp

themes = [
    '​​ 𝗥𝗔𝗡𝗗𝗢𝗠 ​​ (DONT WORK)',
    'Повседневная жизнь',
    'DONT WORK',
    'DONT WORK',
    'DONT WORK',
    'DONT WORK',
    'DONT WORK',
    'DONT WORK'
]

cd_walk = CallbackData("theme_choose", "c")
topic_cd = CallbackData("theme", "topic")


def get_options(c) -> List[InlineKeyboardButton]:
    if c == 0:
        return [InlineKeyboardButton(text=themes[i], callback_data=topic_cd.new(topic=themes[i][:10])) for i in range(5)]
    return [InlineKeyboardButton(text=themes[i], callback_data=topic_cd.new(topic=themes[i][:10])) for i in
            range(5, len(themes))]


def dynamic_markup(c):
    markup = InlineKeyboardMarkup()
    buttons = get_options(c)
    left = InlineKeyboardButton(text='◀️', callback_data=cd_walk.new(c=c - 1))
    right = InlineKeyboardButton(text='▶️', callback_data=cd_walk.new(c=c + 1))
    [markup.add(option) for option in buttons]
    markup.row(left, right)
    return markup


@dp.callback_query_handler(cd_walk.filter(), state='*')
async def get_theme(call: CallbackQuery, callback_data: dict):
    try:
        c = int(callback_data.get('c'))
        if c < 0:
            c = 1
        elif c > 1:
            c = 0
        template = Template(open('handlers/templates/choosing.html').read())
        await call.message.edit_text(text=template.render(),
                                     parse_mode='HTML',
                                     reply_markup=dynamic_markup(c))
    except Exception:
        raise


@dp.callback_query_handler(text='start_task')
async def start_training(call: CallbackQuery):
    template = Template(open('handlers/templates/choosing.html').read())
    await call.message.edit_text(text=template.render(),
                                 parse_mode='HTML',
                                 reply_markup=dynamic_markup(0))



