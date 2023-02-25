import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from status import get_file_status, convert_to_streamable_video


# Initialize Pyrogram client
app = Client("my_bot")


# Handler for /start command
@app.on_message(filters.command("start"))
def start_command_handler(client: Client, message: Message):
    message.reply_text("Hello! I'm a bot that can convert and compress videos. Just send me a video and let me do my magic!")


# Handler for /convert command
@app.on_message(filters.command("convert"))
def convert_command_handler(client: Client, message: Message):
    # Get chat ID and file ID of video message
    chat_id = message.chat.id
    file_id = message.video.file_id
    file_name = message.video.file_name

    # Get path to download directory
    download_dir = app.download_media(message=message)

    # Convert video to streamable format
    streamable_path = convert_to_streamable_video(chat_id, file_id, file_name, download_dir)

    # Send converted video to chat
    message.reply_video(video=streamable_path)


# Handler for /status command
@app.on_message(filters.command("status"))
def status_command_handler(client: Client, message: Message):
    # Get chat ID and file ID of video message
    chat_id = message.chat.id
    file_id = message.video.file_id

    # Get status of file conversion and upload
    status_msg = get_file_status(app, chat_id, file_id)

    # Send status message to chat
    message.reply_text(status_msg)


# Run bot
app.run()
