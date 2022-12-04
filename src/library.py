import random
import requests
import datetime
import wikipedia


def get_prices(coins):
    string = ""
    separator = ","
    arr = list(coins.keys())
    src = f"https://api.coingecko.com/api/v3/simple/price?ids={separator.join(arr)}&vs_currencies=usd"
    r = requests.get(src)
    data = r.json()

    for i, name in enumerate(arr):
        try:
            if name == "bostrom":
                price = round(data[name]["usd"] * 10**9, 2)

            else:
                price = data[name]["usd"]

            string += f"{coins[name]}: ${str(price)}\n"

        except Exception:
            print(f"Problem {name}!")

    return string


def get_date():
    today = datetime.date.today()
    return '{}.{}.{}\n'.format(today.day, today.month, today.year)


def get_stat(url):
    try:
        r = requests.get(url)
        data = {}
        data['height'] = r.json()['height']
        data['cyberlinks'] = r.json()['result']['cyberlinks']
        data['particles'] = r.json()['result']['particles']

        return data

    except Exception:
        return {}


def gen_stat(url, name):
    data = get_stat(url)

    height = "height: {}".format(data["height"])
    cyberlinks = "cyberlinks: {}".format(data["cyberlinks"])
    particles = "particles: {}".format(data["particles"])

    text = f"`{name} {get_date()}\n{height}\n{cyberlinks}\n{particles}`"
    return text


def get_scramble():
    scramble_length = random.randint(25, 28)
    moves = ["R", "R'", "R2", "L", "L'", "L2",
             "U", "U'", "U2", "D", "D'", "D2",
             "F", "F'", "F2", "B", "B'", "B2"]
    scramble = ""

    for i in range(0, scramble_length):
        random_move = random.randint(0, len(moves) - 1)

        if i > 0:
            while moves[random_move][0] == prev_move[0]:
                random_move = random.randint(0, len(moves) - 1)

        scramble += " " + moves[random_move]
        prev_move = moves[random_move]

    return scramble.strip()


def get_weather(city, appid):
    city = city[9:]

    try:
        r = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={appid}")
        data = r.json()
        lat = round(data[0]["lat"])
        lon = round(data[0]["lon"])

    except Exception:
        return "Sorry, there is no such city."

    else:
        q = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}")
        data = q.json()

        main = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        main = main.title()
        temp = str(round(temp - 273.15)) + '°C'
        wind = str(round(wind)) + ' m/s'
        humidity = str(humidity) + '%'

        return f"Main: {main}\nTemp: {temp}\nWind: {wind}\nHumidity: {humidity}"


def get_wiki(text):
    try:
        wikipedia.set_lang("ru")
        ny = wikipedia.page(text[6:])

        return ny.url

    except Exception:
        try:
            wikipedia.set_lang("eu")
            ny = wikipedia.page(text[6:])

            return ny.url

        except Exception:
            return "Article not found!"


def get_cont(text):
    try:
        wikipedia.set_lang("ru")
        ny = wikipedia.page(text[9:])
        string = ny.content

        return string[:string.find("\n")]

    except Exception:
        return "Content not found!"


def get_celebration():
    today = datetime.date.today()
    days = int(format(today, '%j'))

    if today.day == 31 and today.month == 1:
        return "Happy Birthday Python!"

    elif today.day == 26 and today.month == 7:
        return "Happy Birthday Rust!"

    elif today.day == 25 and today.month == 8:
        return "Happy Birthday Linux!"

    elif today.day == 27 and today.month == 9:
        return "Happy Birthday GNU!"

    elif days == 256:
        return "Programmer's Day!"

    elif today.day == 16 and today.month == 3:
        return "Happy Birthday Mastodon"

    else:
        return "There is no holiday today."
