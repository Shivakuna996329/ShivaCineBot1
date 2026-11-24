from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio, json, os

TOKEN = "9024688197:AAEjBeilIPk2HITI2BlYKsxFkddvmIeVOdY"
CHANNEL_ID = -1004462126560
INVITE_LINK = "https://t.me/+WjDfE5AE888xNDQ1"
ADMIN_ID = 870250861

FILE_DB = "files.json"
if os.path.exists(FILE_DB):
    with open(FILE_DB, "r") as f:
        FILES = json.load(f)
else:
    FILES = {}

def save_files():
    with open(FILE_DB, "w") as f:
        json.dump(FILES, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton("📢 Join Channel", url=INVITE_LINK)]]
    await update.message.reply_text("Hi Mama! Welcome! 👋\nFile kavali ante peru type cheyyi.", reply_markup=InlineKeyboardMarkup(buttons))

async def check_join(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def auto_save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    name = (update.message.caption or "").lower().strip()
    file_id = None
    if update.message.document:
        file_id = update.message.document.file_id
    elif update.message.video:
        file_id = update.message.video.file_id
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
    if file_id and name:
        FILES[name] = file_id
        save_files()
        await update.message.reply_text(f"✅ Save Ayipoyindhi mama!\nPeru: `{name}`", parse_mode="Markdown")
    elif file_id:
        await update.message.reply_text("Caption lo peru rayi mama, appude save avuthundi.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    user_id =
