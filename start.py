import os
import random
from collections import deque
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

load_dotenv()  # загрузка значений переменных из файла .env

# Чтение значения переменной TOKEN из переменных среды
TOKEN = os.getenv('TOKEN')
# Чтение значения переменной OPERATOR1_CHAT_ID из переменных среды
OPERATOR1_CHAT_ID = os.getenv('OPERATOR1_CHAT_ID')
# Чтение значения переменной OPERATOR2_CHAT_ID из переменных среды
OPERATOR2_CHAT_ID = os.getenv('OPERATOR2_CHAT_ID')

# Инициализация очереди
queue = deque()

# Добавление сообщения в очередь
def add_message_to_queue(update: CallbackContext, context: CallbackContext):
    message = update.message
    queue.append(message)

# Распределение сообщений по операторам
def distribute_messages_to_operators(context: CallbackContext):
    # Получение списка доступных операторов
    operator_list = get_available_operators()
    if not operator_list:
        return
    # Извлечение следующего сообщения из очереди
    message = queue.popleft()
    # Получение индекса оператора, к которому будет направлено сообщение
    operator_index = get_next_operator_index(operator_list)
    # Отправка сообщения оператору
    operator_chat_id = operator_list[operator_index]['chat_id']
    context.bot.send_message(chat_id=operator_chat_id, text=message.text)

# Получение списка доступных операторов
def get_available_operators():
    # Возвращаем фиктивный список операторов с их именами и chat_id
    return [
        {'name': 'Operator 1', 'chat_id': OPERATOR1_CHAT_ID},
        {'name': 'Operator 2', 'chat_id': OPERATOR2_CHAT_ID}
    ]

# Получение индекса следующего оператора для отправки сообщения
def get_next_operator_index(operator_list):
    # Возвращаем случайный индекс оператора из списка
    return random.randint(0, len(operator_list)-1)

# Создание и запуск бота
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Добавление обработчиков команд
def start_handler(update: CallbackContext, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вас приветствует BitobmenSupport! Чем мы можем Вам помочь?")

dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(MessageHandler(Filters.text, add_message_to_queue))

# Запуск бота и запуск распределения сообщений по операторам
updater.start_polling()
job_queue = updater.job_queue
job_queue.run_repeating(distribute_messages_to_operators, interval=1, context=updater)
