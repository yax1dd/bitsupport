import telebot

# Создаем экземпляр бота
bot = telebot.TeleBot('5956351118:AAGynDsw7uIfed6FkrZugT7yRJa99dH6tz4')  # замените 'TOKEN' на ваш токен бота

# Определяем обработчик для команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет, я BitobmenSupport!')

# Запускаем бота
bot.polling()
