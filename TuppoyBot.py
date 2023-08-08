import telebot
from Configurations import curs, Token
from Extensions import ConvertionException, Convertor

bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Здравствуйте! Для того чтобы начать введите: \n<имя валюты, цену которой хотите узнать> \ <имя второй валюты для расчета курса> \ <количество единиц> \ <список доступных валют: /values>"
    bot.send_message(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные курсы валюты:'
    for i in curs.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Много параметров')

        quote, base, amount = values
        total_base = Convertor.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()