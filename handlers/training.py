import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from jinja2 import Template

from handlers.choose_theme import themes
from handlers.choose_theme import topic_cd
from handlers.states import GetAnswers
from loader import dp, bot

GIF_COUNTDOWN = 'static/gifs/Обратный отсчет 3-2-1-0.gif'
GIF_PREPARATION = 'static/gifs/Preparation 20 sec.mp4'
GIF_RECORDING = 'static/gifs/Recording 40 sec.mp4'
TASK_TEMPLATE = 'handlers/templates/task_text.html'


def get_keyboard(button_text):
    return InlineKeyboardMarkup(InlineKeyboardButton(text=button_text, callback_data="completed"))


def get_topic(callback_data):
    topic = callback_data.get('topic')
    for option in themes:
        if topic in option:
            return option


async def send_audio(chat, audio_file):
    with open(audio_file, 'rb') as audio:
        await bot.send_audio(chat_id=chat.id, audio=audio)


@dp.callback_query_handler(topic_cd.filter(), state='*')
async def start_training(call: CallbackQuery, callback_data: dict, state: FSMContext):
    topic = get_topic(callback_data)

    with open(GIF_COUNTDOWN, 'rb') as gif:
        message_gif = await bot.send_animation(chat_id=call.message.chat.id, animation=gif)
    await asyncio.sleep(4)
    await bot.delete_message(chat_id=message_gif.chat.id, message_id=message_gif.message_id)

    with open(TASK_TEMPLATE) as template_file:
        template = Template(template_file.read())
    await call.message.answer(template.render(), parse_mode='HTML')

    with open(GIF_PREPARATION, 'rb') as gif:
        message_gif = await bot.send_animation(chat_id=call.message.chat.id, animation=gif)
    await asyncio.sleep(20)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=message_gif.message_id)

    await send_audio(call.message.chat, f"static/scripts/{topic}/1.ogg")
    await send_audio(call.message.chat, f"static/scripts/{topic}/2.ogg")

    with open(GIF_RECORDING, 'rb') as gif:
        message_gif = await bot.send_animation(
            chat_id=call.message.chat.id, animation=gif, reply_markup=get_keyboard('Уже закончил!'))
    await state.update_data(message_id=message_gif.message_id, topic=topic)
    await GetAnswers.first_question.set()


@dp.message_handler(content_types=['voice'], state=GetAnswers.first_question)
async def voice_first(message: Message, state: FSMContext):
    data = await state.get_data()
    topic = data.get('topic')
    await bot.delete_message(chat_id=message.chat.id, message_id=data.get('message_id'))

    await send_audio(message.chat, f"static/scripts/{topic}/3.ogg")

    with open(GIF_RECORDING, 'rb') as gif:
        message_gif = await bot.send_animation(
            chat_id=message.chat.id, animation=gif, reply_markup=get_keyboard('Уже закончил!'))
    await state.update_data(message_id=message_gif.message_id)
    await GetAnswers.second_question.set()


@dp.message_handler(content_types=['voice'], state=GetAnswers.second_question)
async def voice_second(message: Message, state: FSMContext):
    data = await state.get_data()
    topic = data.get('topic')
    await bot.delete_message(chat_id=message.chat.id, message_id=data.get('message_id'))

    await send_audio(message.chat, f"static/scripts/{topic}/4.ogg")

    with open(GIF_RECORDING, 'rb') as gif:
        message_gif = await bot.send_animation(
            chat_id=message.chat.id, animation=gif, reply_markup=get_keyboard('Уже закончил!'))
    await state.update_data(message_id=message_gif.message_id)
    await GetAnswers.third_question.set()


@dp.message_handler(content_types=['voice'], state=GetAnswers.third_question)
async def voice_third(message: Message, state: FSMContext):
    data = await state.get_data()
    topic = data.get('topic')
    await bot.delete_message(chat_id=message.chat.id, message_id=data.get('message_id'))

    await send_audio(message.chat, f"static/scripts/{topic}/5.ogg")

    with open(GIF_RECORDING, 'rb') as gif:
        message_gif = await bot.send_animation(
            chat_id=message.chat.id, animation=gif, reply_markup=get_keyboard('Уже закончил!'))
    await state.update_data(message_id=message_gif.message_id)
    await GetAnswers.fourth_question.set()


@dp.message_handler(content_types=['voice'], state=GetAnswers.fourth_question)
async def voice_fourth(message: Message, state: FSMContext):
    data = await state.get_data()
    topic = data.get('topic')
    await bot.delete_message(chat_id=message.chat.id, message_id=data.get('message_id'))

    loading_message = await bot.send_message(chat_id=message.chat.id, text='Подтягиваем данные')
    for i in range(20):
        await asyncio.sleep(0.1)
        await loading_message.edit_text(text=f'Подтягиваем данные{"." * (i % 3 + 1)}')
