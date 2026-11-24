from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio, json, os

TOKEN = "9024688197:AAEpOE7gcixRAfNI68LKdqy0o2Sx9wcBVk0"
CHANNEL_ID = -1004462126560
INVITE_LINK = "https://t.me/+WjDfE5AE888xNDQ1"
ADMIN_ID = 870250861  # Ikkada nee ID pettu

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
    await update.message.reply_text(
        "Hi Mama! Welcome! 👋\nFile kavali ante peru type cheyyi.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def check_join(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# BOT KI FILE PAMPITHE AUTO SAVE AVUTHUNDI
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
    user_id = update.message.from_user.id
    if not await check_join(user_id, context):
        await update.message.reply_text(
            "Mundhu Channel lo Join Avvandi mama 👇",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📢 Join Channel", url=INVITE_LINK)]])
        )
        return
    if text in FILES:
        sent = await update.message.reply_document(FILES[text], caption="Nee File Ready! 10 min lo delete avuthundi.")
        await asyncio.sleep(600)
        try:
            await sent.delete()
        except:
            pass
    else:
        await update.message.reply_text("Ee peru tho file ledu mama.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text(f"Total Files: {len(FILES)}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.PHOTO, auto_save_file))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot Running...")
app.run_polling()
