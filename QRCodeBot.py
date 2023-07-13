import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import urllib.parse
import validators
import json
with open('keys.json') as file:
    data = json.load(file)
TOKEN = data['TOKEN']
URL_QR_CODE_API = data['URL_QR_CODE_API']
URL_CUTT_API = data['URL_CUTT_API']
KEY_CUTT_API = data['KEY_CUTT_API']

bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Получить QR code'))
keyboard.add(KeyboardButton('О проекте'))

def get_shorter_url(url):
    params = {'key': KEY_CUTT_API,
              'short': url}
    response = requests.get(url=URL_CUTT_API, params=params).json()
    return response['url']['shortLink']

@bot.message_handler(regexp='Получить QR code')
def send_welcome(message):
    text = 'Отправь мне размер и содержимое QR кода через пробел (150 пример)'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(regexp='О проекте')
def send_about(message):
    text = 'Бот позволяет получить QR код!\n'
    text += 'QRCodeApi https://goqr.me\n'
    text += 'URLCuttApi https://cutt.ly\n'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(content_types='text')
def send_QR_code(message):
    if message.text != "Получить QR code" and message.text != "О проекте":
        size = message.text.split()[0]
        data = message.text.split()[1]
        print(data)
        if validators.url(data):
            data = get_shorter_url(data)
        params = {
                'size': f'{size}x{size}',
                'data': data
                }
        bot.send_photo(message.chat.id, URL_QR_CODE_API+ '?' + urllib.parse.urlencode(params), reply_markup=keyboard)



bot.infinity_polling()
