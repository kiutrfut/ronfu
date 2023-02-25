import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message

from status import get_file_status, convert_to_streamable_video


# Environment variables
API_ID = os.environ.get("7068313")
API_HASH = os.environ.get("d7446aca34e84b8539a1a8817630d1b5")
BOT_TOKEN = os.environ.get("5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk")


# Create a Pyrogram client instance
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Command to check the status of a file
@app.on_message(filters.command("status"))
def status_command_handler(client: Client, message: Message):
    # Get the file status
    file_path = message.reply_to_message.document.file_name
    status_msg = get_file_status(file_path)
    
    # Reply with the status message
    message.reply_text(status_msg)


# Command to convert a file to streamable video format
@app.on_message(filters.command("convert"))
def convert_command_handler(client: Client, message: Message):
    # Download the file and get its path
    file_path = client.download_media(message.reply_to_message)
    
    # Convert the file to streamable video format
    converted_file_path = convert_to_streamable_video(file_path)
    
    # Reply with the converted file
    message.reply_document(document=converted_file_path)
    
    
# Run the client
app.run()
