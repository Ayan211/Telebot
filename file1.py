import telebot
from config import currencies, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Введите команду в следующем формате: \n<имя валюты> \
<в какую валюту перевести> <количество переводимой валюты> ' \
'\nСписок всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def currency_help(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in currencies.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def exchange(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров')
        quote, base, amount = values
        api_res = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as error:
        bot.reply_to(message, f'Команда не обработана\n{error}')
    else:
        text = f'Результат конвертации: {amount} {quote} - {api_res} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
