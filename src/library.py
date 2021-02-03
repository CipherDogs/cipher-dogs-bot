import requests
import datetime

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
