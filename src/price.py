import requests

def price(arr):
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