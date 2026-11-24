import os, json, telebot
from flask import Flask
from threading import Thread

BOT_TOKEN = "9024688197:AAFtkM59aNK-hE1lgokBPmFA2vL56qig1t4"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

CHANNEL_ID = -1004462126560
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

@bot.channel_post_handler(content_types=['video', 'document', 'photo'])
def learn(post):
    name = ""
    if post.document:
        name = post.document.file_name or ""
    if not name and post.video:
        name = post.video.file_name or ""
    if not name:
        name = post.caption or ""
    name = name.lower().strip()
    if name:
        MOVIES[name] = post.message_id
        save_movies(MOVIES)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Namaste Ra Mama! 🔥\nMovie peru pampu!")

@bot.message_handler(commands=['clear'])
def clear(message):
    global MOVIES
    MOVIES = {}
    save_movies(MOVIES)
    bot.reply_to(message, "Clear chesesanu mama!")

@bot.message_handler(commands=['list'])
def list_movies(message):
    if not MOVIES:
        bot.reply_to(message, "Naku emi gurthu ledhu mama! Channel lo movie forward cheyyi!")
        return
    text = "Naku gurthu unnavi:\n\n"
    for n in MOVIES.keys():
        text += f"- {n}\n"
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True)
def all_movies(message):
    movie = message.text.lower().strip()
    for name, msg_id in MOVIES.items():
        if movie in name:
            bot.reply_to(message, "Dorikindhi mama! Pampisthunnanu... 📥")
            try:
                bot.forward_message(message.chat.id, CHANNEL_ID, msg_id)
            except Exception as e:
                bot.reply_to(message, f"Error: {e}")
            return
    bot.reply_to(message, "Movie dorakaledhu mama...")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
