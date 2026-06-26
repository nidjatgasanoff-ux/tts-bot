import asyncio
import os
import tempfile
import edge_tts
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]
VOICE = "ru-RU-SvetlanaNeural"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь мне любой текст, и я озвучу его 🎙️"
    )

async def tts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return

    await update.message.reply_text("⏳ Озвучиваю...")

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tmp_path = f.name

    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(tmp_path)

        with open(tmp_path, "rb") as audio:
            await update.message.reply_audio(audio, filename="speech.mp3")
    finally:
        os.unlink(tmp_path)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tts_handler))

if __name__ == "__main__":
    app.run_polling()
