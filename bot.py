# t.me/Sokil_info_bot

import telebot
import sqlite3
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode=None)

@bot.message_handler(commands=["start"])
def start_action(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Создать кошик 1')
    button2 = types.KeyboardButton('Создать кошик 2')
    button3 = types.KeyboardButton('Создать кошик 3')
    button4 = types.KeyboardButton('Так-ні')

    markup.add(button1,button2,button3,button4)
    bot.send_message(message.chat.id,"Вітаю, {0.first_name}! \nОбирить ім'я кошика та додайтt до нього об'єкти для випадкового вибіру".format(message.from_user), reply_markup=markup)

    #connect DB and create table
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
        id INTEGER UNIQUE,
        user_first_name TEXT,
        user_last_name TEXT,
        cart1 TEXT,
        cart2 TEXT,
        cart3 TEXT
    )""")

    #check ID in field
    people_id = message.chat.id
    people_firstname = message.chat.first_name
    people_lastname = message.chat.last_name
    cart1 = []
    cart2 = []
    cart3 = []
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        #add values in field
        purchases = [(people_id),
                     (people_firstname),
                     (people_lastname),
                     (cart1),
                     (cart2),
                     (cart3)]
        cursor.execute("INSERT INTO login_id VALUES(?,?,?,?,?,?)", purchases)
        connect.commit()

@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Создать кошик 1':
            bot.send_message(message.chat.id,'1')
        if message.text == 'Создать кошик 2':
            bot.send_message(message.chat.id,'2')
        if message.text == 'Создать кошик 3':
            bot.send_message(message.chat.id,'3')

        elif message.text == 'Так-ні':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)



bot.polling(none_stop = True)





