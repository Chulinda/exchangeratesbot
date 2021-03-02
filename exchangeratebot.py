import requests
import telebot
import matplotlib.pyplot as plt
import datetime


TOKEN = '1684692359:AAH7eD7SREn_l1B60Tt4LweQiNos53Cp-ms'

bot = telebot.TeleBot(TOKEN)

all_currencies = []

def get_latest_usd_rates():
    global rates
    try:
        r = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
    except Exception as ex:
        print(ex.__class__.__name__)
    r = r.json()
    rates = r['rates']


def all_curr():
    global all_currencies
    try:
        r = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
    except Exception as ex:
        print(ex.__class__.__name__)
    r = r.json()
    rates = r['rates']
    for key in rates:
        all_currencies.append(key)


def get_currency_value(val, from_currency, to_currency):
    global rates
    try:
        r = requests.get(f'https://api.exchangeratesapi.io/latest?symbols={from_currency},{to_currency}')
    except Exception as ex:
        print(ex.__class__.__name__)
    r = r.json()
    rates = r['rates'][to_currency]
    rates = rates * float(val)


def get_history(base, symbol, start_at, end_at):
    x = []
    y = []
    try:
        r = requests.get(f'https://api.exchangeratesapi.io/history?start_at={start_at}&end_at={end_at}&base={base}&symbols={symbol}')
    except Exception as ex:
        print(ex.__class__.__name__)
    r = r.json()
    rates = r['rates']
    for key in rates:
        y.append(rates[key][symbol])
        x.append(key)
    f = open('out.jpg','wb')
    plt.plot(x,y)
    plt.grid()
    plt.savefig("graph.png")



@bot.message_handler(commands=["start"])
def start(message):
    all_curr()
    bot.send_message(message.chat.id, 'Привет. Используйте команду /list чтобы посмотреть список валют,конвертированных в USD. ' + '\n' +
    '/exchange 10 USD to CAD - увидеть конвертацию во вторую валюту' + '\n' +
    '/history USD/GBP - график валюты за последние 7 дней')



@bot.message_handler(commands=["list", "lst"])
def start(message):
    get_latest_usd_rates()
    for key in rates:
        bot.send_message(message.chat.id, key + ' ' + str(round(rates[key], 2)))



@bot.message_handler(commands=["exchange"])
def get_currency(message):
    mess = message.text.split()
    value = mess[1]
    from_currency = mess[2]
    to_currency = mess[-1]
    if from_currency not in all_currencies:
        bot.send_message(message.chat.id, 'валюты ' + from_currency + ' не существует')
    elif to_currency not in all_currencies:
        bot.send_message(message.chat.id, 'валюты ' + to_currency + ' не существует')
    else:
        get_currency_value(value, from_currency, to_currency)
        bot.send_message(message.chat.id, str(round(rates, 2)))



@bot.message_handler(commands=["history"])
def histoty(message):
    global all_currencies
    mess = message.text.split() #history USD/CAD
    end_at = str(datetime.datetime.now()).split()[0]
    start_at = end_at.replace(end_at.split('-')[-1], str(datetime.datetime.now().day - 7))
    currencies = mess[1].split('/')
    base = currencies[0]
    symbol = currencies[1]
    if base not in all_currencies:
        bot.send_message(message.chat.id, 'валюты ' + base + ' не существует')
    elif symbol not in all_currencies:
        bot.send_message(message.chat.id, 'валюты ' + symbol + ' не существует')
    else:
        get_history(base, symbol, start_at, end_at)
        img = open('graph.png', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()




if __name__ == '__main__':
    bot.polling(none_stop = True)