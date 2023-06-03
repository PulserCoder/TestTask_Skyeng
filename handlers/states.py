from aiogram.dispatcher.filters.state import State, StatesGroup


class GetAnswers(StatesGroup):
    first_question = State('first_question')
    second_question = State('second_question')
    third_question = State('third_question')
    fourth_question = State('fourth_question')
