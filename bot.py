import logging
import os
import youtube_dl
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    try:
        video_file = download_video(url)
        with open(video_file, 'rb') as video:
            update.message.reply_video(video, progress=upload_progress)
    except Exception as e:
        update.message.reply_text(f"An error occurred: {e}")

# Define a function to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a video link and I'll download it for you!")

# Main function to run the bot
def main():
    # Replace 'YOUR_TOKEN' with your bot's API token
    updater = Updater("YOUR_TOKEN", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()