import telebot


## DEBUG: ключі в основному коді зберігти не можна!!!
## DEBUG: потрібно створити конфіг
bot = telebot.TeleBot("1211817785:AAEh4cQB_QXeVAzTubblyazFrcoXoszAQwE")

## Створюємо клавіатуру
buttons = telebot.types.ReplyKeyboardMarkup()
buttons.row("Привітатися", "Інша клавіатура")
buttons.row("Добавити товар", "Продати товар")


## Створюємо інлайн - клавіатуру
inline = telebot.types.InlineKeyboardMarkup()
tmp1 = telebot.types.InlineKeyboardButton(text="button1", callback_data="id1")
tmp2 = telebot.types.InlineKeyboardButton(text="button2", callback_data="id2")
inline.add(tmp1, tmp2)


@bot.message_handler(commands=['start'])
def hellower(message):
    bot.reply_to(message, 'Hello, word', reply_markup=buttons)

## Кнопака 1 - привітатися
@bot.message_handler(func=lambda msg: msg.text == "Привітатися")
def hey(message):
    bot.send_message(message.chat.id, "Ти натиснув кнопку привітатися")



## Кнопка 2 - Інша клавіатура
@bot.message_handler(func=lambda msg: msg.text == "Інша клавіатура")
def hey(message):
    bot.send_message(message.chat.id, "Ще одна менюшка", reply_markup = inline)



@bot.message_handler(content_types=['text'])
def eho(message):
    bot.send_message(message.chat.id, message.text, reply_markup=buttons)





if __name__ == '__main__':
    bot.polling()
