import telebot
import json
import sqlite3
from sqlite3 import Error
from telebot import types
import threading
import time
import os



with open('config.json', 'r') as file:
    config = json.load(file)

bot_token = config['bot_token']
ip_list = config['ip_list']

bot = telebot.TeleBot(bot_token)

# Function to send status to a specific subscriber
def send_status(chat_id, message):
    try:
        bot.send_message(chat_id, message)
    except telebot.apihelper.ApiTelegramException as e:
        # Handle the exception (e.g., log the error)
        print(f"Failed to send message to user {chat_id}: {e}")
# Function to send a welcome message to new users
def send_welcome_message(chat_id):
    welcome_message = "Welcome to Mware support bot!"
    bot.send_message(chat_id, welcome_message)
def setup_database():
    with sqlite3.connect('subscribers.db') as conn:
        cursor = conn.cursor()
        # Create the 'users' table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY
            )
        ''')
        conn.commit()
# Function to monitor IPs and send updates to all subscribers
def monitor_ips():
    while True:
        for val in ip_list:
            time.sleep(0.2)
            response = os.system('ping -c 3 ' + val)
            if response == 0:
                print(val + ' is up!')
                # Send status update to all subscribers
                #with sqlite3.connect('subscribers.db') as conn:
                #    cursor = conn.cursor()
                #    cursor.execute('SELECT * FROM users')
                #    subscribers = cursor.fetchall()
                #for subscriber in subscribers:
                #    send_status(subscriber[0], val + ' is up')
            else:
                print(val + ' is down!')
                with sqlite3.connect('subscribers.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM users')
                    subscribers = cursor.fetchall()
                for subscriber in subscribers:
                    send_status(subscriber[0], val + ' is down!')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_new_user(message):
    user_id = message.chat.id
    if message.text == '/subscribe':
        with sqlite3.connect('subscribers.db') as conn:
            cursor = conn.cursor()
            print("tryin to add new user",user_id)
            cursor.execute('INSERT OR IGNORE INTO users (chat_id) VALUES (?)', (user_id,))
            conn.commit()
        send_welcome_message(user_id)  # Send the welcome message to the new user
    else :
        send_welcome_message(user_id)  # Send the welcome message to the new user


# Start monitoring in a separate thread

monitor_thread = threading.Thread(target=monitor_ips)
monitor_thread.start()

# Start the bot
bot.polling()
