import asyncio
import os
import tempfile
import edge_tts
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]
VOICE = "ru-RU-SvetlanaNeural"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь текст — озвучу 🎙️")

async def tts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return
    await update.message.reply_text("⏳ Озвучиваю...")
    tmp = tempfile.mktemp(suffix=".mp3")
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await asyncio.wait_for(communicate.save(tmp), timeout=30)
        with open(tmp, "rb") as f:
            await update.message.reply_audio(f)
    except asyncio.TimeoutError:
        await update.message.reply_text("❌ Timeout. Попробуй ещё раз.")
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
