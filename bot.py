import datetime
import os
import requests
import schedule
import telebot
import threading
import time

bot = telebot.TeleBot(token=os.getenv('TOKEN'))
data = {'cyber_russian_community': 0, 'fuckgoogle': 0}


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id, 'CipherDogsBot\nFuck Google! Fuck Twitter! Fuck Web2.0')


@bot.message_handler(func=lambda message: message.chat.username == 'cyber_russian_community', content_types=['new_chat_members'])
def send_sticker_ru(message):
    bot.send_sticker(
        message.chat.id, 'CAACAgIAAxkBAAJAXV-ZAjfq6sotbN3e5_Nc-NMc3RWlAAJWAQACK9RLC9RAtYotQ8NPGwQ')
    if data[message.chat.username] != 0:
        bot.delete_message(
            message.chat.id, data[message.chat.username])
    data[message.chat.username] = message.message_id + 1


@bot.message_handler(func=lambda message: message.chat.username == 'fuckgoogle', content_types=['new_chat_members'])
def send_sticker_en(message):
    bot.send_sticker(
        message.chat.id, 'CAACAgIAAxkBAAJAhl-ZZlpBtcyICOlr_VyWthXoch_7AAIYAQACK9RLC7eumetzzfY-GwQ')
    if data[message.chat.username] != 0:
        bot.delete_message(
            message.chat.id, data[message.chat.username])
    data[message.chat.username] = message.message_id + 1


def get_date():
    today = datetime.date.today()
    return '{}.{}.{}\n'.format(today.day, today.month, today.year)


def print_statistics():
    r = requests.get('https://api.cyber.cybernode.ai/index_stats')
    linksCount = r.json()['result']['linksCount']
    cidsCount = r.json()['result']['cidsCount']
    accountsCount = r.json()['result']['accountsCount']

    text = '`statistics {}\ncyberlinks: {}\ncontent ids: {}\naccounts: {}`'.format(get_date(),
                                                                                   linksCount, cidsCount, accountsCount)

    bot.send_message('@cyber_russian_community', text, parse_mode='Markdown')
    bot.send_message('@fuckgoogle', text, parse_mode='Markdown')


def run_func():
    schedule.every().day.at("16:00").do(print_statistics)

    while True:
        schedule.run_pending()
        time.sleep(1)


th = threading.Thread(target=run_func, args=())
th.start()

bot.polling(True)
