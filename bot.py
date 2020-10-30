import os
import requests
import telebot

bot = telebot.TeleBot(token=os.getenv('TOKEN'))
last_sticker = {'cyber_russian_community': 0, 'fuckgoogle': 0}


@bot.message_handler(func=lambda message: message.chat.username == 'cyber_russian_community', content_types=['new_chat_members'])
def send_sticker_ru(message):
    bot.send_sticker(
        message.chat.id, 'CAACAgIAAxkBAAJAXV-ZAjfq6sotbN3e5_Nc-NMc3RWlAAJWAQACK9RLC9RAtYotQ8NPGwQ')
    if last_sticker[message.chat.username] != 0:
        bot.delete_message(
            message.chat.id, last_sticker[message.chat.username])
    last_sticker[message.chat.username] = message.message_id + 1


@bot.message_handler(func=lambda message: message.chat.username == 'fuckgoogle', content_types=['new_chat_members'])
def send_sticker_en(message):
    bot.send_sticker(
        message.chat.id, 'CAACAgIAAxkBAAJAhl-ZZlpBtcyICOlr_VyWthXoch_7AAIYAQACK9RLC7eumetzzfY-GwQ')
    if last_sticker[message.chat.username] != 0:
        bot.delete_message(
            message.chat.id, last_sticker[message.chat.username])
    last_sticker[message.chat.username] = message.message_id + 1


@bot.message_handler(commands=['statistics'])
def statistics(message):
    r = requests.get('https://api.cyber.cybernode.ai/index_stats')
    linksCount = r.json()['result']['linksCount']
    cidsCount = r.json()['result']['cidsCount']
    accountsCount = r.json()['result']['accountsCount']
    bot.send_message(message.chat.id, '`cyberlinks: {}\ncontent ids: {}\naccounts: {}`'.format(
        linksCount, cidsCount, accountsCount), parse_mode='Markdown')


bot.polling()
