import requests

def price(arr):
    r = requests.get('https://www.bw.com/exchange/config/controller/website/pricecontroller/getassistprice')
    data = r.json()
    string = ''
    for i in range(len(arr)):
        try:
            price = data['datas']['usd'][arr[i]]
            string_coin = arr[i]
            string = string + string_coin.upper() + ': ' + price + '$' + '\n'
        except:
            print('Error')
    return string
