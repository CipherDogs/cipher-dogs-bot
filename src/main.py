import os
import requests
import schedule
import telebot
import threading
import time
from library import get_prices, get_statistics, get_scramble, get_date

bot = telebot.TeleBot(token=os.getenv('TOKEN'))
coins = ["bitcoin", "ethereum", "monero", "polkadot", "kusama", "uniswap", "wownero", "kulupu", "dogecoin"]
last_message = {'cyber_russian_community': 0, 'fuckgoogle': 0}
last_statistics = {'linksCount': 0, 'particles': 0, 'accountsCount': 0,}


def delete_message(message):
    try:
        if last_message[message.chat.username] != 0:
            bot.delete_message(message.chat.id, last_message[message.chat.username])
        last_message[message.chat.username] = message.message_id + 1
    except:
        last_message[message.chat.username] = 0


def print_statistics():
    data = get_statistics()

    linksCount = ''
    particles = ''
    accountsCount = ''

    if last_statistics['linksCount'] == 0:
        linksCount = 'cyberlinks: {}'.format(data['linksCount'])
    else:
        diff = int(data['linksCount']) - int(last_statistics['linksCount'])
        if diff > 0:
            linksCount = 'cyberlinks: {} (+{})'.format(data['linksCount'], diff)
        else:
            linksCount = 'cyberlinks: {} ({})'.format(data['linksCount'], diff)

    if last_statistics['particles'] == 0:
        particles = 'particles: {}'.format(data['particles'])
    else:
        diff = int(data['particles']) - int(last_statistics['particles'])
        if diff > 0:
            particles = 'particles: {} (+{})'.format(data['particles'], diff)
        else:
            particles = 'particles: {} ({})'.format(data['particles'], diff)

    if last_statistics['accountsCount'] == 0:
        accountsCount = 'accounts: {}'.format(data['accountsCount'])
    else:
        diff = int(data['accountsCount']) - int(last_statistics['accountsCount'])
        if diff > 0:
            accountsCount = 'accounts: {} (+{})'.format(data['accountsCount'], diff)
        else:
            accountsCount = 'accounts: {} ({})'.format(data['accountsCount'], diff)

    last_statistics['linksCount'] = data['linksCount']
    last_statistics['particles'] = data['particles']
    last_statistics['accountsCount'] = data['accountsCount']

    text = '`cyber statistics {}\n{}\n{}\n{}`'.format(get_date(), linksCount, particles, accountsCount)

    bot.send_message('@cyber_russian_community', text, parse_mode='Markdown')
    bot.send_message('@fuckgoogle', text, parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id, 'CipherDogsBot\nFuck Google! Fuck Twitter! Fuck Web2.0\nhttps://cipherdogs.net/')


@bot.message_handler(func=lambda message: message.chat.username == 'cyber_russian_community', content_types=['new_chat_members'])
def send_sticker_ru(message):
    bot.send_sticker(
        message.chat.id, 'CAACAgIAAxkBAAJAXV-ZAjfq6sotbN3e5_Nc-NMc3RWlAAJWAQACK9RLC9RAtYotQ8NPGwQ')
    delete_message(message)


@bot.message_handler(func=lambda message: message.chat.username == 'fuckgoogle', content_types=['new_chat_members'])
def send_sticker_en(message):
    bot.send_sticker(
        message.chat.id, 'CAACAgIAAxkBAAJAhl-ZZlpBtcyICOlr_VyWthXoch_7AAIYAQACK9RLC7eumetzzfY-GwQ')
    delete_message(message)


@bot.message_handler(commands=['price'])
def price_coins(message):
    bot.send_message(message.chat.id, get_prices(coins))


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Possible commands:\n/price - displays the price of coins\n/cyber_statistics - displays cyber statistics\n/scramble - displays formula for the rubik's cube")


@bot.message_handler(commands=['scramble'])
def scramble(message):
    bot.send_message(message.chat.id, get_scramble())


@bot.message_handler(commands=['cyber_statistics'])
def statistics(message):
    data = get_statistics()

    linksCount = 'cyberlinks: {}'.format(data['linksCount'])
    particles = 'particles: {}'.format(data['particles'])
    accountsCount = 'accounts: {}'.format(data['accountsCount'])

    text = '`cyber statistics {}\n{}\n{}\n{}`'.format(get_date(), linksCount, particles, accountsCount)

    bot.send_message(message.chat.id, text, parse_mode='Markdown')


def run_func():
    schedule.every().day.at("16:00").do(print_statistics)

    while True:
        schedule.run_pending()
        time.sleep(1)


th = threading.Thread(target=run_func, args=())
th.start()


def telegram_polling():
    try:
        bot.polling(none_stop=True, timeout=60)
    except:
        bot.stop_polling()
        time.sleep(10)
        telegram_polling()


telegram_polling()
