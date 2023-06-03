from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def quick_start_markup():
    quick_start = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Начать!", callback_data='quick_start')
    quick_start.add(button)
    return quick_start


def faq_markup():
    faq = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton(text="А как это задание выглядит на ЕГЭ?", callback_data='faq_show_task')
    button_2 = InlineKeyboardButton(text="А какие критерии оценивания?", callback_data='faq_criteria')
    button_4 = InlineKeyboardButton(text="Кодификатор", web_app=WebAppInfo(
        url='https://synergy.ru/edu/ege/ege_2023/anglijskij_yazyik/demoversii_i_kimyi/kodifikator_ege_po_anglijskomu_yazyiku_2023'))
    button_3 = InlineKeyboardButton(text="Все понятно, погнали 😎", callback_data='start_task')
    faq.add(button_1).row(button_2).row(button_4).row(button_3)
    return faq


def back_faq_menu():
    back_menu = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text='Назад', callback_data='back_to_faq')
    back_menu.add(back_button)
    return back_menu
