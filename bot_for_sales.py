import telebot
import collections
import configparser
import sql_bot

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config['Telebot']['Token']
bot = telebot.TeleBot(TOKEN)

#рівні юзера для кнопки "Прихід товару"
START, LVL1, LVL2, LVL3 = 0, 1, 2, 3
LVL4, LVL5 = 4, 5

# словник у якому зберігаємо рівні юзера
dict_with_lvl = collections.defaultdict(lambda: START)
#словник, що тимчасово зберігає введений продук юзера
dict_with_productuser = {}



## Створюємо клавіатуру
markup = telebot.types.ReplyKeyboardMarkup()
markup.row("Добавити товар", "Продати товар")

## Створюємо клавіатуру для виходу
markup_exit = telebot.types.ReplyKeyboardMarkup()
markup_exit.row("Exit")

@bot.message_handler(func=lambda msg: msg.text == "Exit")
def exit(message):
    if dict_with_lvl[message.chat.id]:
        del dict_with_lvl[message.chat.id]

    if dict_with_productuser.get(message.chat.id, False):
        del dict_with_productuser[message.chat.id]

    bot.send_message(message.chat.id, "Ви успішно вийшли", reply_markup=markup)



@bot.message_handler(commands=['start'])
def hellower(message):
    #привітання
    bot.reply_to(message, 'Привіт! Тут ти можеш обліковувати продукти в своєму магазині', reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == "Добавити товар")
def add_product(message):

    dict_with_lvl[message.chat.id] = LVL1  #переводимо юзера на новий рівень

    bot.send_message(message.chat.id, "Введи назву товару:", reply_markup=markup_exit)


@bot.message_handler(func=lambda msg: dict_with_lvl[msg.chat.id] == LVL1)
def product(message):

    #тимчасово зберігаємо назву товару в базу даних
    dict_with_productuser[message.chat.id] = message.text

    if sql_bot.check_product(message.text)  == True:
        #переводимо на рівень введення кількості
        dict_with_lvl[message.chat.id] = LVL3
        bot.send_message(message.chat.id, "Введи кількість для товару",reply_markup=markup_exit)

    else:
        #переводимо на рівень введеня один виміру
        dict_with_lvl[message.chat.id] = LVL2
        bot.send_message(message.chat.id, "Введи одинці виміру", reply_markup=markup_exit)



@bot.message_handler(func=lambda msg: dict_with_lvl[msg.chat.id] == LVL2)
def unit(message):

    #створюємо запис в таблиці sql :product:
    product = dict_with_productuser[message.chat.id]
    unit = message.text
    result = sql_bot.insert_product(product, unit)
    if result:
        dict_with_lvl[message.chat.id] = LVL3
        bot.send_message(message.chat.id, "Введи кількість для товару", reply_markup=markup_exit)
    else:
        del dict_with_lvl[message.chat.id]
        bot.send_message(message.chat.id, "Щось пішло не так. Спробуйе ще раз", reply_markup=markup_exit)




@bot.message_handler(func=lambda msg: dict_with_lvl[msg.chat.id] == LVL3)
def qty(message):

    product = dict_with_productuser[message.chat.id]

    try:
        qty = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Введіть коректну кількість!",  reply_markup=markup_exit)
        dict_with_lvl[message.chat.id] = LVL3
    else:
        if sql_bot.insert_sales(product, qty):

            del dict_with_lvl[message.chat.id]                      #del user lvl

            #виводимо в  консоль таблицю даних
            sql_bot.select_product()
            sql_bot.select_sales()                                  # DEBUG: del this

            bot.send_message(message.chat.id, "Товар добавлено", reply_markup=markup)
        else:
            del dict_with_lvl[message.chat.id]
            bot.send_message(message.chat.id, "Упс",  reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == "Продати товар")
def add_product(message):

    dict_with_lvl[message.chat.id] = LVL4  #переводимо юзера на новий рівень

    bot.send_message(message.chat.id, "Введи назву товару:", reply_markup=markup_exit)


@bot.message_handler(func=lambda msg: dict_with_lvl[msg.chat.id] == LVL4)
def product(message):

    #тимчасово зберігаємо назву товару в базу даних
    dict_with_productuser[message.chat.id] = message.text

    if sql_bot.check_product(message.text)  == True:
        #переводимо на рівень введення кількості
        dict_with_lvl[message.chat.id] = LVL5
        bot.send_message(message.chat.id, "Введи кількість для товару",reply_markup=markup_exit)
    else:
        bot.send_message(message.chat.id, "Товар відсутній")
        del dict_with_lvl[message.chat.id]


@bot.message_handler(func=lambda msg: dict_with_lvl[msg.chat.id] == LVL5)
def qty(message):

    product = dict_with_productuser[message.chat.id]

    try:
        qty = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Введіть коректну кількість!",  reply_markup=markup_exit)
        dict_with_lvl[message.chat.id] = LVL5
    else:
        if sql_bot.insert_sales(product, -qty):

            del dict_with_lvl[message.chat.id]                      #del user lvl

            #виводимо в  консоль таблицю даних
            sql_bot.select_product()
            sql_bot.select_sales()                                  # DEBUG: del this

            bot.send_message(message.chat.id, "Товар продано", reply_markup=markup)
        else:
            del dict_with_lvl[message.chat.id]
            bot.send_message(message.chat.id, "Упс",  reply_markup=markup)









if __name__ == '__main__':
    bot.polling()
