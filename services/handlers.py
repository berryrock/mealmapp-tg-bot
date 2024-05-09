from . import dbhelper, texts

import telebot
from telebot import types
import time


def handle_start(message, bot):
    # Создаем запись о пользователе в базе данных
    try:
        dbhelper.add_user(message.chat.id, message.from_user.username,
            message.from_user.first_name, message.from_user.last_name)
    except:
        raise Exception

    # Обновляем этап онбординга пользователя на первый
    try:
        dbhelper.update_onboarding_stage(message.chat.id, 1)
    except:
        raise Exception

    # Создаем inline клавиатуру с кнопкой "Продолжить"
    markup = types.InlineKeyboardMarkup()
    continue_button = types.InlineKeyboardButton(texts.ONBOARDING_STAGE_1_BUTTON.get('RU','ONBOARDING_STAGE_1_BUTTON'),
        callback_data='continue')
    markup.add(continue_button)

    # Отправляем приветственное сообщение с клавиатурой
    bot.send_message(message.chat.id, texts.ONBOARDING_STAGE_1.get('RU','ONBOARDING_STAGE_1'),
        reply_markup=markup)


# Обработчик нажатия на inline кнопку "Продолжить"
def handle_continue(callback_query, bot):
    # Удаляем кнопку "Продолжить" из первого сообщения
    bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id)

    # Обновляем этап онбординга пользователя на второй
    dbhelper.update_onboarding_stage(callback_query.message.chat.id, 2)

    # Создаем inline клавиатуру с кнопкой "Начать пользоваться"
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(texts.ONBOARDING_STAGE_2_BUTTON.get('RU','ONBOARDING_STAGE_2_BUTTON'),
        callback_data='start_using')
    markup.add(start_button)

    # Отправляем второе сообщение с инструкцией
    bot.send_message(callback_query.message.chat.id, texts.ONBOARDING_STAGE_2.get('RU','ONBOARDING_STAGE_2'),
        reply_markup=markup)


# Обработчик нажатия на inline кнопку "Начать пользоваться"
def handle_start_using(callback_query, bot):
    # Обновляем этап онбординга пользователя на завершение
    try:
        dbhelper.update_onboarding_stage(callback_query.message.chat.id, 3)
    except:
        raise Exception

    # Удаляем кнопку "Начать пользоваться" из второго сообщения
    bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id)

    # Отправляем сообщение о завершении онбординга
    bot.send_message(callback_query.message.chat.id, texts.ONBOARDING_STAGE_DONE.get('RU','ONBOARDING_STAGE_DONE'))
    time.sleep(1)
    bot.send_message(callback_query.message.chat.id, texts.DEMO_WARNING.get('RU','DEMO_WARNING'))


def handle_text_message(message, bot):
    # TBD
    pass
    '''markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(telebot.types.InlineKeyboardButton("Ссылка на трекер", web_app=telebot.types.WebAppInfo(config.WEB_APP_URL)))
    bot.reply_to(message, message.text, reply_markup=markup)'''


def handle_callback_query(call, bot):
    if call.data == 'continue':
        handle_continue(call, bot)
    elif call.data == 'start_using':
        handle_start_using(call, bot)


def handle_web_app_data(message, bot):
    # TBD
    pass
    '''
    try:
        web_app_data = json.loads(message.web_app_data.data)
        bot.send_message(message.chat.id, "Спасибо за обратную связь!")
        time.sleep(1)
        name = web_app_data.get('name', 'Без имени')
        if len(name) > 0:
            bot.send_message(message.chat.id, name)
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON")
    '''


def handle_web_app_save_daily_meals_request_data(request, bot):
    callback_query_id = request.json['callback_query_id']
    kcal = request.json['kcal']
    fats = request.json['fats']
    carbs = request.json['carbs']
    proteins = request.json['proteins']
    # TBD: send meals to backend
    # TBD: add history button to message
    bot.answer_web_app_query(callback_query_id, {
        'type': 'article',
        'id': callback_query_id,
        'title': 'Успешно обновлено',
        'input_message_content': {
            'message_text': text.TRACKER_SAVED + f'{kcal} / {proteins} / {fats} / {carbs}',

        }
    })
