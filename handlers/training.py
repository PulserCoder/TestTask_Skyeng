import asyncio
from config import Config

import openai
import whisper
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
openai.api_key = Config.CHAT_GPT

def get_keyboard(button_text):
    return InlineKeyboardMarkup(InlineKeyboardButton(text=button_text, callback_data="completed"))

def get_back():
    a =  InlineKeyboardMarkup()
    b = InlineKeyboardButton(text='Вернуться назад', callback_data="back")
    a.add(b)
    return a
def recognize_voice(response):
    with open("audio.ogg", 'wb') as f:
        f.write(response.read())
    model = whisper.load_model("tiny")
    result = model.transcribe("audio.ogg")
    return result["text"]




def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,  # The conversation history up to this point, as a list of dictionaries
        max_tokens=400,  # The maximum number of tokens (words or subwords) in the generated response
        stop=None,  # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,  # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content


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
    voice = message.voice
    text = '-'
    if voice:
        voice_file_id = voice.file_id
        voice_file = await bot.get_file(voice_file_id)
        voice_file_url = voice_file.file_path
        response = await bot.download_file(voice_file_url)
        text = await asyncio.get_running_loop().run_in_executor(None, recognize_voice, response)





    data = await state.get_data()
    topic = data.get('topic')
    await bot.delete_message(chat_id=message.chat.id, message_id=data.get('message_id'))

    await send_audio(message.chat, f"static/scripts/{topic}/3.ogg")

    with open(GIF_RECORDING, 'rb') as gif:
        message_gif = await bot.send_animation(
            chat_id=message.chat.id, animation=gif, reply_markup=get_keyboard('Уже закончил!'))
    await state.update_data(message_id=message_gif.message_id)
    await state.update_data(question_1=text)
    await GetAnswers.second_question.set()


@dp.message_handler(content_types=['voice'], state=GetAnswers.second_question)
async def voice_second(message: Message, state: FSMContext):
    data = await state.get_data()
    voice = message.voice
    text = '-'
    if voice:
        voice_file_id = voice.file_id
        voice_file = await bot.get_file(voice_file_id)
        voice_file_url = voice_file.file_path
        response = await bot.download_file(voice_file_url)
        text = await asyncio.get_running_loop().run_in_executor(None, recognize_voice, response)

    topic = data.get('topic')
    await bot.delete_message(chat_id=message.chat.id, message_id=data.get('message_id'))

    await send_audio(message.chat, f"static/scripts/{topic}/4.ogg")

    with open(GIF_RECORDING, 'rb') as gif:
        message_gif = await bot.send_animation(
            chat_id=message.chat.id, animation=gif, reply_markup=get_keyboard('Уже закончил!'))
    await state.update_data(message_id=message_gif.message_id)
    await state.update_data(question_2=text)
    await GetAnswers.third_question.set()


@dp.message_handler(content_types=['voice'], state=GetAnswers.third_question)
async def voice_third(message: Message, state: FSMContext):
    voice = message.voice
    text = '-'
    if voice:
        voice_file_id = voice.file_id
        voice_file = await bot.get_file(voice_file_id)
        voice_file_url = voice_file.file_path
        response = await bot.download_file(voice_file_url)
        text = await asyncio.get_running_loop().run_in_executor(None, recognize_voice, response)
    await state.update_data(question_3=text)




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
    voice = message.voice
    text = '-'
    if voice:
        voice_file_id = voice.file_id
        voice_file = await bot.get_file(voice_file_id)
        voice_file_url = voice_file.file_path
        response = await bot.download_file(voice_file_url)
        text = await asyncio.get_running_loop().run_in_executor(None, recognize_voice, response)
    await state.update_data(question_4=text)

    data = await state.get_data()
    topic = data.get('topic')
    await bot.delete_message(chat_id=message.chat.id, message_id=data.get('message_id'))

    mes = loading_message = await bot.send_message(chat_id=message.chat.id, text='Подтягиваем данные')
    for i in range(20):
        await asyncio.sleep(0.1)
        await loading_message.edit_text(text=f'Подтягиваем данные{"." * (i % 3 + 1)}')
    d = await state.get_data()
    text = f"Вопрос: What is your favourite food? Why do you like it so much? Can you cook it?'\nСтудент: {d.get('question_1')}\nВопрос: Have your food preferences changed over time? Why or why not?\nСтудент: {d.get('question_2')}\nВопрос: Do you think your favourite food is healthy? Is there any unhealthy food that you like?\nСтудент: {d.get('question_3')}\nВопрос: How often do you eat your favourite food? Would you like to eat it more often?\nСтудент: {d.get('question_4')}"
    message_log = [{"role": "system", "content": "Дай разбаловку на ответы ЕГЭ 4 задание устная часть. Учитывая то что ты проверяющий на ЕГЭ в России. Сейчас пришлю диалог студента и проводящего экзамен. Как ответ отправь просто количество баллов"}, {"role": "user", "content": text}]
    response = await asyncio.get_running_loop().run_in_executor(None, send_message, message_log)
    await bot.send_message(chat_id=message.chat.id, text='312', reply_markup=get_back())
    await mes.delete()




