import os
import telebot

bot = telebot.TeleBot(token = os.getenv('TOKEN'))

@bot.message_handler(content_types=['new_chat_members'])
def send_sticker(message):
	username = message.chat.username
	if username == 'cyber_russian_community':
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJAXV-ZAjfq6sotbN3e5_Nc-NMc3RWlAAJWAQACK9RLC9RAtYotQ8NPGwQ')
	elif username == 'fuckgoogle':
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJAhl-ZZlpBtcyICOlr_VyWthXoch_7AAIYAQACK9RLC7eumetzzfY-GwQ')
		
bot.polling()