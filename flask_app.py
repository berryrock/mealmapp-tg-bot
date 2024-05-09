import config
from services import handlers, dbhelper

from flask import Flask, request
import telebot


# Указываем токен вашего бота
TOKEN = config.TOKEN

# Создаем объекты Flask и бота
app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)
dbhelper.create_users_table()


# Обработка запросов
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return "ok", 200


# Обработчик вебхука
@app.route(config.WEBHOOK_PATH, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return '', 200


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    handlers.handle_start(message, bot)


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def text_message_handler(message):
    handlers.handle_text_message(message, bot)


# Обработчик нажатия на inline кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    handlers.handle_callback_query(call, bot)


# Обработчик отправленных данных от веб-приложения через KeyboardButton
@bot.message_handler(content_types=['web_app_data'])
def web_app_data_handler(message):
    handlers.handle_web_app_data(message, bot)


# Обработчик данных от веб-приложения бота
@app.route('/web-data', methods=['POST'])
def web_app_data_post():
    handlers.handle_web_app_post_request_data(request, bot)
    return "ok", 200



if __name__ == '__main__':
    # Устанавливаем вебхук
    bot.remove_webhook()
    bot.set_webhook(url=config.HOST+config.WEBHOOK_PATH)
    # Запускаем веб-сервер Flask
    app.run(host='0.0.0.0', port=8443, debug=True)
