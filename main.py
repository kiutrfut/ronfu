import os
import logging
import mimetypes
import ffmpeg
import requests

from pyrogram import Client, filters
from pyrogram.types import Message

from status import get_file_status, convert_to_streamable_video


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(name)

# Get environment variables
TOKEN = os.environ.get("5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk")
API_ID = int(os.environ.get("7068313"))
API_HASH = os.environ.get("d7446aca34e84b8539a1a8817630d1b5")

# Create Pyrogram client
app = Client("ronfu", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH)

# Define start command handler
@app.on_message(filters.command("start"))
def start_command_handler(client: Client, message: Message):
    message.reply_text("Hi there! I can help you convert videos to streamable formats. Just send me a video file and I'll do the rest.")

# Define status command handler
@app.on_message(filters.command("status"))
def status_command_handler(client: Client, message: Message):
    if message.reply_to_message is None or message.reply_to_message.media is None:
        message.reply_text("Please reply to a video file.")
        return

    file_id = message.reply_to_message.document.file_id
    file_name = message.reply_to_message.document.file_name
    status_msg = get_file_status(client, message.chat.id, file_id, file_name)

    message.reply_text(status_msg)

# Define convert command handler
@app.on_message(filters.command("convert"))
def convert_command_handler(client: Client, message: Message):
    if message.reply_to_message is None or message.reply_to_message.media is None:
        message.reply_text("Please reply to a video file.")
        return

    # Get file info
    file_id = message.reply_to_message.document.file_id
    file_name = message.reply_to_message.document.file_name
    mime_type = message.reply_to_message.document.mime_type

    # Download file
    file_path = client.download_media(message=message.reply_to_message)

    # Check if file is already streamable
    if mime_type.startswith("video/"):
        message.reply_text("This video is already streamable.")
        return

    # Convert to streamable format
    streamable_path = convert_to_streamable_video(client, message.chat.id, file_id, file_name, file_path)
    if streamable_path is None:
        message.reply_text("Failed to convert video.")
        return

    # Upload converted video
    streamable_file = open(streamable_path, "rb")
    streamable_msg = client.send_video(
        chat_id=message.chat.id,
        video=streamable_file,
        duration=0,
        thumb=None,
        caption=f"Converted version of {file_name}"
    )
    streamable_file.close()

    # Delete original video and converted video
    os.remove(file_path)
    os.remove(streamable_path)

# Run the app
app.run()
