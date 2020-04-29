import telebot

bot = telebot.TeleBot("948207399:AAExhoGew7b703Ki2S3TTlAUaAT5WKiYlXw")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()
