import os
import telebot

bot = telebot.TeleBot(token = os.getenv('TOKEN'))

@bot.message_handler(func=lambda message: message.chat.username == 'cyber_russian_community', content_types=['new_chat_members'])
def send_sticker_ru(message):
	bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJAXV-ZAjfq6sotbN3e5_Nc-NMc3RWlAAJWAQACK9RLC9RAtYotQ8NPGwQ')

@bot.message_handler(func=lambda message: message.chat.username == 'fuckgoogle', content_types=['new_chat_members'])
def send_sticker_en(message):
	bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJAhl-ZZlpBtcyICOlr_VyWthXoch_7AAIYAQACK9RLC7eumetzzfY-GwQ')

bot.polling()