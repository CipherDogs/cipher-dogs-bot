import os
import time
import telebot
import schedule
import threading
from library import *


bot = telebot.TeleBot(token=os.getenv('TOKEN'))
last_message = {'cyber_russian_community': 0, 'fuckgoogle': 0}
last_statistics = {'height': 0, 'cyberlinks': 0, 'particles': 0}
coins = [
    "bitcoin",
    "ethereum",
    "polkadot",
    "kusama",
    "cosmos",
    "osmosis",
    "monero",
    "wownero",
    "kulupu",
    "juno-network",
    "stargaze",
    "secret",
    "acala",
    "moonbeam",
    "phala-network",
]


def delete_message(message):
    try:
        if last_message[message.chat.username] != 0:
            bot.delete_message(
                message.chat.id,
                last_message[message.chat.username]
            )
        last_message[message.chat.username] = message.message_id + 1
    except Exception:
        last_message[message.chat.username] = 0


def print_statistics():
    data = get_statistics()

    height = ''
    cyberlinks = ''
    particles = ''

    if last_statistics['height'] == 0:
        height = f"height: {data['height']}"
    else:
        height = f"height: {last_statistics['height']}"

    if last_statistics['cyberlinks'] == 0:
        cyberlinks = f"cyberlinks: {data['cyberlinks']}"
    else:
        diff = int(data['cyberlinks']) - int(last_statistics['cyberlinks'])
        if diff > 0:
            cyberlinks = f"cyberlinks: {data['cyberlinks']} (+{diff})"
        else:
            cyberlinks = f"cyberlinks: {data['cyberlinks']} ({diff})"

    if last_statistics['particles'] == 0:
        particles = f"particles: {data['particles']}"
    else:
        diff = int(data['particles']) - int(last_statistics['particles'])
        if diff > 0:
            particles = f"particles: {data['particles']} (+{diff})"
        else:
            particles = f"particles: {data['particles']} ({diff})"

    last_statistics['height'] = data['height']
    last_statistics['cyberlinks'] = data['cyberlinks']
    last_statistics['particles'] = data['particles']

    text = f"""`cyber statistics {get_date()}\n
            {height}\n{cyberlinks}\n{particles}`"""

    bot.send_message('@cyber_russian_community', text, parse_mode='Markdown')
    bot.send_message('@fuckgoogle', text, parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id,
        """CipherDogsBot\n
        Fuck Google! Fuck Twitter! Fuck Web2.0\n
        https://cipherdogs.net/"""
        )


@bot.message_handler(
    func=lambda message: message.chat.username == 'cyber_russian_community',
    content_types=['new_chat_members'])
def send_sticker_ru(message):
    bot.send_sticker(
        message.chat.id,
        'CAACAgIAAxkBAAJAXV-ZAjfq6sotbN3e5_Nc-NMc3RWlAAJWAQACK9RLC9RAtYotQ8NPGwQ')
    delete_message(message)


@bot.message_handler(
    func=lambda message: message.chat.username == 'fuckgoogle',
    content_types=['new_chat_members'])
def send_sticker_en(message):
    bot.send_sticker(
        message.chat.id,
        'CAACAgIAAxkBAAJAhl-ZZlpBtcyICOlr_VyWthXoch_7AAIYAQACK9RLC7eumetzzfY-GwQ')
    delete_message(message)


@bot.message_handler(commands=['price'])
def price_coins(message):
    bot.send_message(message.chat.id, get_prices(coins))


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        """Possible commands:
            /price - displays the price of coins
            /cyber_statistics - displays cyber statistics
            /find - find article in wikipedia
        """
    )


@bot.message_handler(commands=['scramble'])
def scramble(message):
    bot.send_message(message.chat.id, get_scramble())


@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(
        message.chat.id,
        get_weather(message.text, appid=os.getenv('APPID'))
    )


@bot.message_handler(commands=["find"])
def handle_page(message):
    bot.send_message(message.chat.id, get_wiki(message.text))


@bot.message_handler(commands=["content"])
def handle_cont(message):
    bot.send_message(message.chat.id, get_cont(message.text))

@bot.message_handler(commands=["day"])
def handle_day(message):
    bot.send_message(message.chat.id, get_celebration())


@bot.message_handler(commands=['cyber_statistics'])
def statistics(message):
    data = get_statistics()

    height = 'height: {}'.format(data['height'])
    cyberlinks = 'cyberlinks: {}'.format(data['cyberlinks'])
    particles = 'particles: {}'.format(data['particles'])

    text = f"""`cyber statistics {get_date()}\n
            {height}\n{cyberlinks}\n{particles}`"""

    bot.send_message(message.chat.id, text, parse_mode='Markdown')


def run_func():
    # schedule.every().day.at("16:00").do(print_coins, coins)
    schedule.every().day.at("16:00").do(print_statistics)

    while True:
        schedule.run_pending()
        time.sleep(1)


th = threading.Thread(target=run_func, args=())
th.start()


def telegram_polling():
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception:
        bot.stop_polling()
        time.sleep(10)
        telegram_polling()


telegram_polling()
