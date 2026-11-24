import os, json, telebot
from flask import Flask
from threading import Thread

BOT_TOKEN = "9024688197:AAFtkM59aNK-hE1lgokBPmFA2vL56qig1t4"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

CHANNEL_ID = -1003758874620
MOVIES_FILE = "movies.json"

def load_movies():
    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, "r") as f:
            return json.load(f)
    return {}
def save_movies(data):
    with open(MOVIES_FILE, "w") as f:
        json.dump(data, f)

MOVIES = load_movies()

@app.route('/')
def home():
    return "ShivaCineBot is Live!"

# Bot - File Peru nundi Movie Peru teesukuntundi
@bot.channel_post_handler(content_types=['video', 'document'])
def learn_from_channel(post):
    name = ""
    if post.document:
        name = post.document.file_name or ""
    elif post.video:
        name = post.video.file_name or ""
    if not name:
        name = post.caption or ""
    name = name.lower().strip()
    if name:
        MOVIES[name] = post.message_id
        save_movies(MOVIES)
        print(f"Learned: {name}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Namaste Ra Mama! 🔥\nMovie peru pampu!")

@bot.message_handler(func=lambda m: True)
def all_movies(message):
    movie = message.text.lower().strip()
    for name, msg_id in MOVIES.items():
        # User Kalki ante - File lo Kalki unte chalu
        if movie in name:
            bot.reply_to(message, f"Super! Dorikindhi Ra Mama! 🔥\nFile pampisthunnanu... 📥")
            bot.copy_message(message.chat.id, CHANNEL_ID, msg_id)
            return
    bot.reply_to(message, "Movie dorakaledhu mama... 🔍")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
