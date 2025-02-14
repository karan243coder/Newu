import logging
import os
import youtube_dl
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a function to show download progress
def download_progress_hook(d):
    if d['status'] == 'downloading':
        percent = d['downloaded_bytes'] / d['total_bytes'] * 100
        logger.info(f"Downloading: {percent:.2f}%")

# Define a function to download video
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'progress_hooks': [download_progress_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_file = ydl.prepare_filename(info_dict)
    return video_file

# Define a function to show upload progress
def upload_progress(current, total):
    percent = current / total * 100
    logger.info(f"Uploading: {percent:.2f}%")

# Define a function to handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    try:
        video_file = download_video(url)
        with open(video_file, 'rb') as video:
            await update.message.reply_video(video, progress=upload_progress)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

# Define a function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a video link and I'll download it for you!")

# Main function to run the bot
def main():
    # Replace 'YOUR_TOKEN' with your bot's API token
    application = ApplicationBuilder().token("YOUR_TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()