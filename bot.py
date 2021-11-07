import requests
import math
import telebot

API_KEY = 'HERE GOES MY TELEGRAM API TOKEN'
CURRENT_WEATHER_API_KEY = 'HERE GOES MY WEATHERMAP API TOKEN'
TYPES_LIST = ['text', 'audio', 'document', 'photo', 'sticker', 'video', 'location', 'contact']
bot = telebot.TeleBot(API_KEY)


def get_current_weather(api_key, lat, lon):
    """
    take care of getting the weather from specific coordinates
    :return dictionary of the parameters current_temperature, max_temperature,
    min_temperature, feels like temperature, humidity and sky's condition
    (clear, rain ect.)
    """

    # where to take weather from
    url = f"http://api.openweathermap.org/data/2.5/weather?lat=" \
          f"{lat}&lon={lon}&appid={api_key}"

    response = requests.get(url).json()

    # calculate the temperature in c
    current_temp = response['main']['temp'] - 273.5
    current_temp = math.floor(current_temp)
    feels_like = response['main']['feels_like'] - 273.5
    feels_like = math.floor(feels_like)
    humidity = response['main']['humidity']
    sky = response['weather'][0]['main']  # the clarity of the sky

    return {'temp': current_temp,
            'feels_like': feels_like,
            'humidity': humidity,
            'sky': sky
            }


def is_snowy(weather):
    return weather['sky'] == "Snow"


def is_rainy(weather):
    return weather['sky'] == "Rain"


def is_cold_and_rainy(weather):
    return weather['sky'] == "Rain" and weather['temp'] <= 18


def is_freezy(weather):
    return weather['temp'] < 10 or weather['feels_like'] < 10


def is_cold(weather):
    return 10 <= weather['temp'] <= 18 or 10 <= weather['feels_like'] <= 19


def is_warm(weather):
    return 18 < weather['temp'] < 26 or 19 < weather['feels_like'] < 24


def is_hot(weather):
    return weather['temp'] >= 26 or weather['feels_like'] >= 24


def choose_clothes(weather):
    if is_snowy(weather):
        return "It's  snowy! do you want to build a snowman?"
    elif is_cold_and_rainy(weather):
        return "It's cold and rainy, take a coat with at least one layer " \
               "underneath"
    elif is_freezy(weather):
        return "It's freezy out there, heavy coat with two layers minimum!"
    elif is_cold(weather):
        return "Its cold outside, consider wear long shirt with sweater above"
    elif is_warm(weather):
        return "It's warm, wear a T-shirt!"
    elif is_hot(weather):
        return "It's hot outside, it's time for tank top and shorts!"
    else:  # unhandled situation
        return "Undefined weather, consider wearing layers so you could " \
               "take them off if necessary"


@bot.message_handler(commands=['start'])
def start(message):
    msg = "Hey! I'm you're new friend, and I'm here to help you choose what " \
          "to wear!"
    bot.reply_to(message, msg)


@bot.message_handler(commands=['help'])
def help_user(message):
    msg = "Hey, do you need help?\n" \
          "I'm a pretty simple bot, so this is all I can do:\n" \
          "If you send me a location, yours or any (MUST be a telegram location)," \
          " I'll tell you what I think you should wear, based on the weather of that location!"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.location is not None:
        lat, lon = message.location.longitude, message.location.latitude
        weather = get_current_weather(CURRENT_WEATHER_API_KEY, lat, lon)
        what_to_wear_message = choose_clothes(weather) + "\n"
        bot.send_message(message.chat.id, what_to_wear_message)


@bot.message_handler(content_types=TYPES_LIST)
def reply(message):
    bot.reply_to(message, "I dont know what to do with that, type /help for "
                          "more info")


bot.polling()
