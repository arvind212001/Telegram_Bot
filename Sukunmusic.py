import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8297448324:AAGsQJPL6UluNTNFP5xwKUmTvlL_BxvCVyA"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Send me a song name and I will play it for you!")

# Handle song search
async def download_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    song_name = update.message.text
    await update.message.reply_text(f"🔎 Searching for: {song_name}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            video = info['entries'][0]
            file_name = ydl.prepare_filename(video)

        await update.message.reply_audio(audio=open(file_name, 'rb'))

        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text("❌ Error downloading song.")
        print(e)

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_song))

    print("🤖 Bot is running...")
    app.run_polling()