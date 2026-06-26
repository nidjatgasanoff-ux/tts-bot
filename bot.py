import os
import tempfile
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь текст — озвучу 🎙️")

async def tts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return
    await update.message.reply_text("⏳ Озвучиваю...")
    tmp = tempfile.mktemp(suffix=".mp3")
    try:
        tts = gTTS(text=text, lang="ru")
        tts.save(tmp)
        with open(tmp, "rb") as f:
            await update.message.reply_audio(f)
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tts_handler))
    app.run_polling()
