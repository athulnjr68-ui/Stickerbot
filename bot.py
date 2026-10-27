import os
import telebot
from PIL import Image
from flask import Flask, request

TOKEN = "8649339714:AAHS7Q9PDnLNN-WJbb8cCJ9ZJD_WB570m0I"
CHANNEL_ID = "@jshshajanansh"
ADMIN_CHAT_ID = 8717387472
APP_URL = "https://stickerbot-9jvt.onrender.com"

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route('/')
def index():
    return "Stickerbot is running!", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ഹായ്! 👋 സ്റ്റിക്കർ അയക്കൂ...")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        
        bot.send_message(CHANNEL_ID, f"New photo from {user_name} (ID: {user_id})")
        bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)
        bot.reply_to(message, "ഫോട്ടോ ലഭിച്ചു! 👍")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL + '/' + TOKEN)
    port = int(os.environ.get("PORT", 10000))
    server.run(host="0.0.0.0", port=port)
