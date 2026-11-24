import os
import telebot
from flask import Flask
from threading import Thread

# Kottha Token - Ikkada Veyyi - Leda Render lo Env lo pettu
BOT_TOKEN = "9024688197:AAFtkM59aNK-hE1lgokBPmFA2vL56qig1t4"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- IKKADA MOVIE LINKS VEYYI MAMA ---
# Channel lo Post paina Right Click > Copy Link chesi ikkada veyyi
MOVIES = {
    "kalki": "https://t.me/c/3758874620/9004",
    "kalki 2898": "https://t.me/shivacinemas/.../Kalki_Post_Link",
    "pushpa": "https://t.me/shivacinemas/.../Pushpa_Post_Link",
}

@app.route('/')
def home():
    return "ShivaCineBot is Live!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Namaste Ra Mama! 🔥\nWelcome to ShivaCineBot!\n\nMovie peru pampu, nenu link isthanu!")

@bot.message_handler(func=lambda m: True)
def all_movies(message):
    movie = message.text.lower().strip()

    # 1. Movie mana list lo unte - Direct Link pampisthundi
    for name, link in MOVIES.items():
        if name in movie:
            bot.reply_to(message, f"Super! Dorikindhi Ra Mama! 🔥\n\nMovie: {message.text}\n\nLink: {link}\n\nEnjoy Mama! 🍿")
            return

    # 2. Lekapothe - Wait ani chepthundi
    bot.reply_to(message, f"Super! Nuvvu adigina movie: {message.text}\n\nLink kosam konchem wait cheyyi mama, nenu velthanu... 🔍\n\nEe movie maa daggara ledu, admin ki cheppanu!")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    print("Bot Started...")
    bot.infinity_polling()
