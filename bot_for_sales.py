import telebot
import collections

## DEBUG: ключі в основному коді зберігти не можна!!!
## DEBUG: потрібно створити конфіг
bot = telebot.TeleBot("")

#рівні юзера, які задаємо числами
START, LVL1, LVL2 = 0, 1, 2


# словник у якому зберігаємо рівні юзера
dict_with_lvlusers = collections.defaultdict(lambda: START)


#словник, що тимчасово зберігає введений продук юзера
dict_with_productuser = {}

#база даних для товару
base_with_product = {}

## Створюємо клавіатуру
markup = telebot.types.ReplyKeyboardMarkup()
markup.row("Добавити товар", "Продати товар")

@bot.message_handler(commands=['start'])
def hellower(message):
    #привітання
    bot.reply_to(message, 'Привіт! Тут ти можеш обліковувати продукти в своєму магазині', reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text == "Добавити товар")
def hey(message):
    #переводимо юзера на новий рівень
    dict_with_lvlusers[message.chat.id] = LVL1
    bot.send_message(message.chat.id, "Введи назву товару:")

@bot.message_handler(func=lambda msg: dict_with_lvlusers[msg.chat.id] == LVL1)
def product(message):
    #переводимо юзера на новий рівень
    dict_with_lvlusers[message.chat.id] = LVL2

    #тимчасово зберігаємо назву товару в базу даних
    dict_with_productuser[message.chat.id] = message.text

    bot.send_message(message.chat.id, "Введи кількість для товару")



@bot.message_handler(func=lambda msg: dict_with_lvlusers[msg.chat.id] == LVL2)
def product(message):
    #Добавив інфу про товар в базу
    product_tmp = dict_with_productuser[message.chat.id]
    if product_tmp in base_with_product:
        #якщо товар є в базі, то сумуємо кількість
        base_with_product[product_tmp] += int(message.text)
    else:
        #якщо товар відсутні, створюємо його
        base_with_product[product_tmp] = int(message.text)

    #обнуляємо рівень юзера
    del dict_with_lvlusers[message.chat.id]

    print(base_with_product) # DEBUG: виводимо в консоль, щоб перевірити коректність

    bot.send_message(message.chat.id, "Товар добавлено")
    bot.send_message("884716148", f"Товар {product_tmp} в кількісті {message.text}")



if __name__ == '__main__':
    bot.polling()
