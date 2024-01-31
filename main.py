from bot_info import TOKEN_API, CHANNEL, NAME_FILE, THROTTLE_DELEY, COOLDOWN_DELEY, SHUTDOWN_DELEY
import json

from datetime import datetime, timedelta
import time

import telebot
from telebot import types

from keyy import markupp
from stickerf import stickers, web, emoji


bot = telebot.TeleBot(TOKEN_API)

CHANNEL_ID = CHANNEL

USER = {}

THROTTLING = {}

CDKEYBORDS = {}

START_TIME = {}

DELTA = timedelta(seconds= THROTTLE_DELEY)
COLLDOWN = timedelta(minutes= COOLDOWN_DELEY)
SHUTDOWNUSER = timedelta(minutes= SHUTDOWN_DELEY)

filename = NAME_FILE


def throttle(f):
    def inner(message):
        if message.chat.id in THROTTLING:
            current_time = datetime.now()
            if current_time - THROTTLING[message.chat.id] > DELTA:
                THROTTLING[message.chat.id] = datetime.now()
                return f(message)

    return inner


def colldown_decorator(f):
    def inner(message):

        if message.chat.id in CDKEYBORDS:
            current_time = datetime.now()
            if current_time - CDKEYBORDS[message.chat.id] > COLLDOWN:
                CDKEYBORDS[message.chat.id] = datetime.now()
                return f(message)
            else:
                bot.send_message(message.chat.id, 'А щоб тебе підняло і гепнуло.')
                bot.send_message(message.chat.id, 'Вже підганяю цього лентюха!!!')
                bot.send_sticker(message.chat.id, sticker=stickers[1])
                return bot.delete_message(message.chat.id, message.message_id)


    return inner


def start_time(f):
    def inner(message):
        if message.chat.id in START_TIME:
            current_time = datetime.now()
            if current_time - START_TIME[message.chat.id] < SHUTDOWNUSER:
                return f(message)
            else:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, 'На жаль, час дії сплинув. Відскануй QR ще раз.')
                bot.send_sticker(message.chat.id, sticker=stickers[2])

    return inner


@bot.message_handler(commands=['start'])
def main(message):
    THROTTLING[message.chat.id] = datetime.now()
    CDKEYBORDS[message.chat.id] = datetime.now() - COLLDOWN
    START_TIME[message.chat.id] = datetime.now()

    with open(filename, 'r') as file:
        data = json.loads(file.read())
    try:
        USER[message.chat.id] = data[message.text.split()[-1]]
    except KeyError:
        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} '
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2])
    else:
        bot.send_message(message.chat.id, 'Привіт я твій особистий помічник ', reply_markup=markupp)
        bot.send_message(message.chat.id, f'{emoji["fox_face"]}')
        bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(func=lambda message: message.text == f'Меню {emoji["fork_knife"]}')
@throttle
@start_time
def menu(message):
    markup = types.InlineKeyboardMarkup()

    btnkitchen = types.InlineKeyboardButton(f'Щось пожерти {emoji["drooling_face"]}', url=web['kitchen'])
    markup.row(btnkitchen)
    btnbar = types.InlineKeyboardButton(f'Дати по буфету {emoji["wine"]}', url=web['bar'])
    btnhookah = types.InlineKeyboardButton(f'КОЛЯНИ {emoji["dashing"]} ', url=web['hookah'])
    markup.row(btnbar, btnhookah)
    bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(func=lambda message: message.text == f'Виклик офіціанта {emoji["person_tiping"]}')
@colldown_decorator
@start_time
def callO(message):
    CDKEYBORDS[message.chat.id] = datetime.now()

    if USER.get(message.chat.id) == '/start':
        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} '
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2])

    elif USER.get(message.chat.id) is not None:
        bot.send_message(CHANNEL_ID, f'Офіціанта за  {USER.get(message.chat.id)}')
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f'Вже біжить як дикий вепр {emoji["snail"]}')
        bot.send_sticker(message.chat.id, sticker=stickers[3])
    else:
        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} '
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2])


@bot.message_handler(func=lambda message: message.text == f'Виклик кальянщика {emoji["dashing"]}')
@colldown_decorator
@start_time
def callH(message):
    CDKEYBORDS[message.chat.id] = datetime.now()

    if USER.get(message.chat.id) == '/start':
        bot.send_message(message.chat.id,f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} ')
        bot.send_sticker(message.chat.id, sticker=stickers[2])

    elif USER.get(message.chat.id) is not None:
        bot.send_message(CHANNEL_ID, f'Кальянщика за  {USER.get(message.chat.id)}')
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f'Вже мчить кабанчиком {emoji["boar"]}')
        bot.send_sticker(message.chat.id, sticker=stickers[6])

    else:
        bot.send_message(
            message.chat.id,
            f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} '
        )
        bot.send_sticker(message.chat.id, sticker=stickers[2])


@bot.message_handler(func=lambda message: message.text == f'Похвалити офіціанта {emoji["parting"]}')
@throttle
@start_time
def tip(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(
        message.chat.id,f'Дякую за похвалу, наші фокси завжди страються заради вашого комфорту {emoji["beating_hearth"]}')
    bot.send_message(CHANNEL_ID, f'Похвалив обслуговування  {USER.get(message.chat.id)}')


@bot.message_handler(func=lambda message: message.text == f'Поскаржитися на офіціанта {emoji["dizzy"]}')
@throttle
@start_time
def complaint(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(CHANNEL_ID, f'Поскаржився  {USER.get(message.chat.id)}')
    bot.send_message(message.chat.id, f'Можеш сказати що саме не так {emoji["fearful"]}')
    bot.register_next_step_handler(message, negative_feedback)


@bot.message_handler(func=lambda message: message.text.startswith("Рахунок"))
@throttle
@start_time
def account(message):
    if USER.get(message.chat.id) == '/start':

        bot.send_message(message.chat.id, f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} ')
        bot.send_sticker(message.chat.id, sticker=stickers[2])

    elif USER.get(message.chat.id) is not None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cash = types.KeyboardButton(f'Готівка {emoji["money_wings"]}')
        cart = types.KeyboardButton(f'Карта {emoji["card"]}')
        markup.row(cash, cart)
        bot.send_message(message.chat.id, 'Оберіть метод оплати ', reply_markup=markup)
        bot.send_sticker(message.chat.id, sticker=stickers[4])
        bot.delete_message(message.chat.id, message.message_id)
        bot.register_next_step_handler(message, check)
    else:
        bot.send_message(message.chat.id,f'{emoji["weary_cat"]} Відскануйте ще раз qr-код і спробуйте знову {emoji["weary_cat"]} ',)
        bot.send_sticker(message.chat.id, sticker=stickers[2])


@bot.message_handler(func=lambda message: message.text == f'Відгук {emoji["speech"]}')
@throttle
@start_time
def response(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'Тиць{emoji["paw"]} ', url=web['feedback_google']))
    bot.send_message(message.chat.id, f'Відгук{emoji["orange_hearth"]}', reply_markup=markup)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler()
@throttle
@start_time
def check(message):
    if message.text.startswith("Готівка"):
        bot.send_message(CHANNEL_ID, f'Рахунок готівкою за {USER.get(message.chat.id)}')

    elif message.text.startswith("Карта"):
        bot.send_message(CHANNEL_ID, f'Рахунок картою {USER.get(message.chat.id)}')

    bot.delete_message(message.chat.id, message.message_id)

    bot.send_message(message.chat.id, f'Вже друкуємо {emoji["memo"]}')
    bot.send_message(message.chat.id, f'До зустрічі я буду чекати на тебе {emoji["beating_hearth"]}',reply_markup = markupp)
    bot.send_sticker(message.chat.id, sticker=stickers[5])


@bot.message_handler()
def negative_feedback(message):
    bot.send_message(CHANNEL_ID, message.text)
    bot.send_message(message.chat.id, f'Дякую за відгук, я обов\'язково прийму відповідні заходи {emoji["man"]}',reply_markup = markupp)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True,skip_pending=True )
        except Exception as e:
            time.sleep(3)
            
