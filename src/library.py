import requests
import datetime
import random


def get_prices(arr):
    string = ''
    for i in range(len(arr)):
        try:
            r = requests.get('https://api.bitfinex.com/v1/pubticker/'+ arr[i] +'usd')
            data = r.json()
            price = data['ask']
            string_coin = arr[i]
            string = string + string_coin.upper() + ': ' + price + '$' + '\n'
        except:
            print('Error')
    return string


def get_date():
    today = datetime.date.today()
    return '{}.{}.{}\n'.format(today.day, today.month, today.year)


def get_statistics():
    r = requests.get('https://api.cyber.cybernode.ai/index_stats')
    linksCount = 'cyberlinks: {}'.format(r.json()['result']['linksCount'])
    cidsCount = 'content ids: {}'.format(r.json()['result']['cidsCount'])
    accountsCount = 'accounts: {}'.format(r.json()['result']['accountsCount'])
    return '`statistics {}\n{}\n{}\n{}`'.format(get_date(), linksCount, cidsCount, accountsCount)


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
