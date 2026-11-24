import os
import telebot
from flask import Flask
from threading import Thread

BOT_TOKEN = "9024688197:AAGk8-kOoGPjzVWP99lJKM7eEELXzQHA4qE"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "ShivaCineBot is Live!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Namaste Ra Mama! 🔥\nWelcome to ShivaCineBot!\n\nMovie peru pampu, nenu link isthanu!")

@bot.message_handler(func=lambda m: True)
def all_movies(message):
    movie = message.text
    bot.reply_to(message, f"Super! Nuvvu adigina movie: {movie}\n\nLink kosam konchem wait cheyyi mama, nenu velthanu... 🔍")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    print("Bot Started...")
    bot.infinity_polling()
