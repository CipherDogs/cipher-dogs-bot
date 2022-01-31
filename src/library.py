import requests
import datetime
import random

def get_prices(arr):
    string = ""
    separator = ","
    src = "https://api.coingecko.com/api/v3/simple/price?ids=" + separator.join(arr) + "&vs_currencies=usd"
    r = requests.get(src)
    data = r.json()
    for i in range(len(arr)):
        price = data[arr[i]]["usd"]
        string_coin = arr[i]
        string += string_coin.title() + ": " + str(price) + "$" + "\n"
    return string


def get_date():
    today = datetime.date.today()
    return '{}.{}.{}\n'.format(today.day, today.month, today.year)


def get_statistics():
    r = requests.get('https://lcd.bostrom.cybernode.ai/graph/graph_stats')
    data = {}
    data['height'] = r.json()['height']
    data['cyberlinks'] = r.json()['result']['cyberlinks']
    data['particles'] = r.json()['result']['particles']
    return data


def get_scramble():
    scramble_length = random.randint(25, 28)
    moves = ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2"]
    scramble = ""
    for i in range(0, scramble_length):
        random_move = random.randint(0, len(moves) - 1)
        if i > 0:
            while moves[random_move][0] == prev_move[0]:
                random_move = random.randint(0, len(moves) - 1)
        scramble += " " + moves[random_move]
        prev_move = moves[random_move]
    return scramble.strip()


def celebration(bot):
    today = datetime.date.today()
    if today.day == 31 and today.month == 1:
        bot.send_message("@tesbot31337", "Happy Birthday Python!")