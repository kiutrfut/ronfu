import os
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.raw.types import InputFile
from pyrogram.types import Message
import time

# Replace with your API_ID and API_HASH
api_id = 7068313
api_hash = "d7446aca34e84b8539a1a8817630d1b5"
app = Client("my_account", api_id=api_id, api_hash=api_hash)


# Convert2 command
def convert2(bot, message):
    if message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document
        if document.mime_type == 'application/pdf':
            try:
                # Download the file using pyrogram
                with app:
                    downloaded_file = app.download_media(message.reply_to_message)
                # Convert the file using ffmpeg
                os.system(f"ffmpeg -loop 1 -i image.jpg -i {downloaded_file} -c:a libfdk_aac -b:a 192k -c:v libx264 -preset ultrafast -shortest -vf scale=w=720:h=-1:force_original_aspect_ratio=decrease {downloaded_file}.mp4")
                # Upload the converted file using pyrogram
                with app:
                    app.send_video(message.chat.id, InputFile(f"{downloaded_file}.mp4"))
                bot.reply_to(message, "File converted to mp4 format.")
                os.remove(downloaded_file)
                os.remove(f"{downloaded_file}.mp4")
            except FloodWait as e:
                time.sleep(e.x)
            except Exception as e:
                bot.reply_to(message, f"Error converting file: {e}")
        else:
            bot.reply_to(message, "Please reply to a PDF document to convert it to mp4 format.")
    else:
        bot.reply_to(message, "Please reply to a PDF document to convert it to mp4 format.")
