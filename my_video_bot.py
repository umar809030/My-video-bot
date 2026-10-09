import telebot
import os
import threading
from flask import Flask
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ================== SETTINGS ==================
BOT_TOKEN = "8617727563:AAEEu7_2pR8YMeclUGfpuNZqisec0Auo1F8"
CHANNEL_USERNAME = "@freepanelbio" 
VIDEO_FILE_ID = "" 

# ================== BOT LOGIC ==================
bot = telebot.TeleBot(BOT_TOKEN)

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("Start"), KeyboardButton("Video"))
    return markup

@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == "Start")
def send_welcome(message):
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "Hello! Video bhejne ke liye neeche 'Video' button dabayein.", reply_markup=main_menu())
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Channel Join Karein ✅", url="https://t.me/freepanelbio"))
        bot.reply_to(message, "Pehle aapko hamara channel join karna hoga, tabhi main video bhej sakta hoon.", reply_markup=markup)

@bot.message_handler(commands=['video'])
@bot.message_handler(func=lambda message: message.text == "Video")
def send_video(message):
    if is_subscribed(message.from_user.id):
        if VIDEO_FILE_ID == "":
            bot.reply_to(message, "Abhi koi video set nahi hai. Kripya admin se kahein ki woh koi video bhejein.")
        else:
            bot.reply_to(message, "Video bhej raha hoon, thoda wait karein...")
            bot.send_video(message.chat.id, VIDEO_FILE_ID)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Channel Join Karein ✅", url="https://t.me/freepanelbio"))
        bot.reply_to(message, "Video dekhne ke liye pehle channel join karein!", reply_markup=markup)

@bot.message_handler(content_types=['video'])
def get_video_id(message):
    global VIDEO_FILE_ID
    VIDEO_FILE_ID = message.video.file_id
    bot.reply_to(message, "Video mil gayi!\n\nAb users 'Video' button dabakar ise paa sakte hain.", reply_markup=main_menu())

# ================== CLOUD SERVER LOGIC ==================
def run_bot():
    print("Bot chal raha hai...")
    bot.infinity_polling()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running successfully!"

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
