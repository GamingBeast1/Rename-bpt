import os
import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image
import os

# Telegram bot token
TOKEN = os.environ.get('6109955170:AAHlRyrIjQcT35a_oZ2MfJ58Ph8Bfr1HHcw', '6109955170:AAHlRyrIjQcT35a_oZ2MfJ58Ph8Bfr1HHcw')

# Rest of the code...

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Telegram bot token (replace with your own bot token)
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'


def start(update, context):
    """Handler for /start command"""
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome! Send me multiple files to rename and add thumbnails.")


def process_files(update, context):
    """Handler for files received"""
    file_ids = [file.file_id for file in update.message.document]
    file_info_list = [context.bot.get_file(file_id) for file_id in file_ids]

    # Process each file
    for file_info in file_info_list:
        file_url = file_info.file_path

        # Download the file
        file_path = os.path.join('downloads', file_info.file_name)
        download_file(file_url, file_path)

        # Rename the file
        new_file_name = 'new_filename.txt'  # Replace with desired new file name
        new_file_path = os.path.join('downloads', new_file_name)
        os.rename(file_path, new_file_path)

        # Generate thumbnail
        thumbnail_path = os.path.join('thumbnails', 'thumbnail.jpg')
        generate_thumbnail(new_file_path, thumbnail_path)

        # Send the renamed file and thumbnail back
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(new_file_path, 'rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(thumbnail_path, 'rb'))


def download_file(file_url, file_path):
    """Download the file from the given URL"""
    response = requests.get(file_url, stream=True)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)


def generate_thumbnail(file_path, thumbnail_path):
    """Generate a thumbnail from the file"""
    image = Image.open(file_path)
    image.thumbnail((256, 256))
    image.save(thumbnail_path)


def main():
    """Main function to start the bot"""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))

    # File handler
    dp.add_handler(MessageHandler(Filters.document & (~Filters.reply), process_files))

    # Start the bot
    updater.start_polling()
    logger.info("Bot started.")

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
