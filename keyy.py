
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from stickerf import emoji

markupp = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton(f'Меню {emoji.get("fork_knife")}')
btn5 = KeyboardButton(f'Рахунок {emoji.get("page")}')
markupp.row(btn1, btn5)
btn2 = KeyboardButton(f'Відгук {emoji.get("speech")}')
btn3 = KeyboardButton(f'Виклик офіціанта {emoji.get("person_tiping")}')
btn4 = KeyboardButton(f'Виклик кальянщика {emoji.get("dashing")}')
btn7 = KeyboardButton(f'Похвалити офіціанта {emoji.get("parting")}')
btn6 = KeyboardButton(f'Поскаржитися на офіціанта {emoji.get("dizzy")}')
markupp.row(btn2, btn3, btn4)
markupp.row(btn7, btn6)
