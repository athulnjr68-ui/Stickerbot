import os
import telebot
from PIL import Image
from flask import Flask, request

TOKEN = "8649339714:AAHS7Q9PDnLNN-WJbb8cCJ9ZJD_WB570m0I"
CHANNEL_ID = "@jshshajanansh"
ADMIN_CHAT_ID = 8717387472
APP_URL = "https://your-app-name.onrender.com"

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@server.route('/', methods=['GET', 'POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ഹായ്! 👋 ഞാൻ 24/7 ലൈവ് ആണ്! എനിക്ക് ഫോട്ടോ അയക്കൂ, സ്റ്റിക്കർ തരാം!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        
        bot.send_message(CHANNEL_ID, f"📸 പുതിയ ഫോട്ടോ!\nഅയച്ച ആൾ: {user_name}\nഐഡി: {user_id}")
        bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)

        bot.reply_to(message, "സ്റ്റിക്കർ തയ്യാറാക്കിക്കൊണ്ടിരിക്കുന്നു... 🔄")
        
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        
        image_path = "temp.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        img = Image.open(image_path)
        img.thumbnail((512, 512))
        
        sticker_path = "sticker.webp"
        img.save(sticker_path, "WEBP")
        
        with open(sticker_path, 'rb') as sticker:
            bot.send_sticker(message.chat.id, sticker)
            
        os.remove(image_path)
        os.remove(sticker_path)
        
    except Exception as e:
        bot.reply_to(message, f"എന്തോ കുഴപ്പം സംഭവിച്ചു: {e}")

@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL + '/' + TOKEN)
    return "Bot is running via webhook!", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8443))
    server.run(host="0.0.0.0", port=port)
