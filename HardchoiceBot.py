#t.me/HardchoiceBot

import telebot
import random
import sqlite3
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode=None)

conn = sqlite3.connect('bot.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS user_values (
               user_id INTEGER,
               value TEXT
               )""")
conn.commit()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'''Привет! Нажмите кнопку, чтобы начать использование бота.
Этот бот поможет тебе сделать случайный выбор.
\nНапример, заполни список напитками,
которые хотелось бы выпить и бот сделает выбор за тебя!''', reply_markup=get_main_keyboard())

def get_main_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('1. Показать список'))
    keyboard.add(telebot.types.KeyboardButton('2. Добавить значение'))
    keyboard.add(telebot.types.KeyboardButton('3. Выдать случайное значение'))
    keyboard.add(telebot.types.KeyboardButton('4. Удалить последнее значение'))
    return keyboard

@bot.message_handler(func=lambda message: message.text == '1. Показать список')
def show_list(message):
    conn = sqlite3.connect('bot.db', check_same_thread=False)
    cursor = conn.cursor()
    user_id = message.chat.id
    cursor.execute('SELECT * FROM user_values WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    if len(rows) > 0:
        values = '\n'.join([row[1] for row in rows])
        bot.send_message(message.chat.id, f'Список значений:\n{values}')
    else:
        bot.send_message(message.chat.id, 'Список пуст.')

@bot.message_handler(func=lambda message: message.text == '2. Добавить значение')
def add_value(message):
    bot.send_message(message.chat.id, 'Введите значение для добавления в список.')
    bot.register_next_step_handler(message, handle_add_value)

def handle_add_value(message):
    user_id = message.chat.id
    value = message.text.strip()
    cursor.execute('INSERT INTO user_values (user_id, value) VALUES (?, ?)', (user_id, value))
    conn.commit()
    bot.send_message(message.chat.id, 'Значение добавлено в список.', reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: message.text == '3. Выдать случайное значение')
def get_random_value(message):
    user_id = message.chat.id
    cursor.execute('SELECT * FROM user_values WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    if len(rows) > 0:
        random_value = random.choice(rows)[1]
        bot.send_message(message.chat.id, f'Случайное значение: {random_value}.')
    else:
        bot.send_message(message.chat.id, 'Список пуст.')

@bot.message_handler(func=lambda message: message.text == '4. Удалить последнее значение')
def delete_last_value(message):
    user_id = message.chat.id
    cursor.execute("SELECT MAX(rowid) FROM user_values WHERE user_id = ?", (user_id,))
    row_id = cursor.fetchone()[0]
    if row_id is None:
        bot.send_message(message.chat.id, 'Список пуст.')
    else:
        cursor.execute("DELETE FROM user_values WHERE rowid=?", (row_id,))
        conn.commit()
        bot.send_message(message.chat.id, 'Последнее значение удалено.', reply_markup=get_main_keyboard())

bot.polling(none_stop = True)
