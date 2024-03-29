import os
import csv
import time
import telebot
import schedule
import threading
from library import *


bot = telebot.TeleBot(token=os.getenv("TOKEN"))
last_message = {"cyber_russian_community": 0, "fuckgoogle": 0}
url_bostrom = "https://lcd.bostrom.cybernode.ai/graph/graph_stats"
url_pussy = "https://lcd.space-pussy.cybernode.ai/graph/graph_stats"
coins = {
    "bitcoin":          "BTC",
    "ethereum":         "ETH",
    "polkadot":         "DOT",
    "kusama":           "KSM",
    "pha":              "PHA",
    "cosmos":           "ATOM",
    "osmosis":          "OSMO",
    "evmos":            "EVMOS",
    "juno-network":     "JUNO",
    "secret":           "SCRT",
    "eos":              "EOS",
    "mina-protocol":    "MINA",
    "the-open-network": "TON",
    "monero":           "XMR",
    "wownero":          "WOW",
    "kulupu":           "KLP",
    "bostrom":          "GBOOT"
}


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


def print_statistics(url, file_name, title):
    data = get_stat(url)
    csv_data = []

    csv_wfile = open(f"{file_name}.csv", "a")
    csv_rfile = open(f"{file_name}.csv", "r")

    csvwriter = csv.writer(csv_wfile)
    csvreader = csv.reader(csv_rfile)

    for row in csvreader:
        csv_data.append(row)

    if csv_data == []:
        csvwriter.writerow(["height", "cyberlinks", "particles"])

    height = ""
    cyberlinks = ""
    particles = ""

    if len(csv_data) <= 1:
        height = f"height: {data['height']}"
        cyberlinks = f"cyberlinks: {data['cyberlinks']}"
        particles = f"particles: {data['particles']}"
        csvwriter.writerow([data['height'], data['cyberlinks'],
                            data['particles']])

    else:
        diff_links = int(data["cyberlinks"]) - int(csv_data[len(csv_data)-1][1])
        diff_part = int(data["particles"]) - int(csv_data[len(csv_data)-1][2])

        height = f"height: {data['height']}"

        if diff_links > 0:
            cyberlinks = f"cyberlinks: {data['cyberlinks']} (+{diff_links})"
        else:
            cyberlinks = f"cyberlinks: {data['cyberlinks']} ({diff_links})"

        if diff_part > 0:
            particles = f"particles: {data['particles']} (+{diff_part})"
        else:
            particles = f"particles: {data['particles']} ({diff_part})"

        csvwriter.writerow([data['height'], data['cyberlinks'],
                            data['particles']])

    csv_wfile.close()
    csv_rfile.close()

    text = f"`{title} {get_date()}\n{height}\n{cyberlinks}\n{particles}`"

    bot.send_message("@cyber_russian_community", text, parse_mode="Markdown")


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(
        message.chat.id,
        "CipherDogsBot\n\
Fuck Google! Fuck Twitter! Fuck Web2.0\n\
https://cipherdogs.net/"
    )


@bot.message_handler(
    func=lambda message: message.chat.username == "cyber_russian_community",
    content_types=["new_chat_members"],
)
def send_sticker_ru(message):
    bot.send_sticker(
        message.chat.id,
        "CAACAgIAAxkBAAJAXV-ZAjfq6sotbN3e5_Nc-NMc3RWlAAJWAQACK9RLC9RAtYotQ8NPGwQ",
    )
    delete_message(message)


@bot.message_handler(commands=["price"])
def price_coins(message):
    bot.send_message(message.chat.id, get_prices(coins))


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(
        message.chat.id,
        "Possible commands:\n\
/price - displays the price of coins\n\
/bostrom_statistics - displays bostrom statistics\n\
/pussy_statistics - displays space pussy statistics\n\
/find - find article in wikipedia"
    )


@bot.message_handler(commands=["scramble"])
def scramble(message):
    bot.send_message(message.chat.id, get_scramble())


@bot.message_handler(commands=["weather"])
def weather(message):
    bot.send_message(
        message.chat.id,
        get_weather(message.text, appid=os.getenv("APPID"))
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

@bot.message_handler(commands=["price_now"])
def price_now(message):
    bot.send_message(message.chat.id, get_now_price(message.text))

@bot.message_handler(commands=["bostrom_statistics"])
def bostrom_statistics(message):
    text = gen_stat(url_bostrom, "bostrom statistics")
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=["pussy_statistics"])
def pussy_statistics(message):
    text = gen_stat(url_pussy, "space pussy statistics")
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def run_func():
    schedule.every().day.at("16:00").do(print_statistics,
                                        url=url_bostrom,
                                        file_name="bostrom",
                                        title="bostrom statistics")
    schedule.every().day.at("16:00").do(print_statistics,
                                        url=url_pussy,
                                        file_name="pussy",
                                        title="space pussy statistics")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)

        except Exception as e:
            print(f"Error {e}!")


th = threading.Thread(target=run_func, args=())
th.start()


def telegram_polling():
    try:
        bot.polling(none_stop=True, timeout=120)

    except Exception:
        bot.stop_polling()
        time.sleep(10)
        telegram_polling()


telegram_polling()
