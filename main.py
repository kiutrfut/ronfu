import os
import time
import shutil
from hurry.filesize import size
from pyrogram import Client, filters
from pyrogram.types import Message
from status import get_status_message

# Create a new Telegram Bot using the Bot Father and get the API token
API_TOKEN = "5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk"

# Create a new Pyrogram client instance
app = Client("my_bot", api_id=7068313, api_hash="d7446aca34e84b8539a1a8817630d1b5", bot_token=API_TOKEN)

# Define the "/start" command handler
@app.on_message(filters.command("start"))
def start_command_handler(client: Client, message: Message):
    # Send a welcome message to the user
    message.reply_text("Hello! I'm a Telegram Bot. Send me a file and type /convert to convert it into a streamable video format.")

# Define the "/convert" command handler
@app.on_message(filters.command("convert"))
def convert_command_handler(client: Client, message: Message):
    # Check if the message contains a file
    if not message.document:
        message.reply_text("Please send a file to convert.")
        return

    # Check if the file is in video format
    if not message.document.mime_type.startswith("video/"):
        message.reply_text("Sorry, I can only convert video files.")
        return

    # Download the file
    message.reply_text("Downloading file...")
    file_path = f"{message.document.file_name}_{message.document.file_id}"
    file = client.download_media(message=message, file_name=file_path)

    # Convert the file
    message.reply_text("Converting file...")
    output_file_path = f"{os.path.splitext(file_path)[0]}.mp4"
    os.system(f"ffmpeg -i '{file}' -codec:v libx264 -profile:v main -preset slow -b:v 500k -maxrate 500k -bufsize 1000k -vf scale=-2:720 -threads 0 -codec:a libfdk_aac -b:a 128k '{output_file_path}'")

    # Delete the original file
    os.remove(file)

    # Send the converted file
    message.reply_text("Sending file...")
    with open(output_file_path, "rb") as f:
        app.send_video(chat_id=message.chat.id, video=f, caption=f"Converted file ({size(os.path.getsize(output_file_path))})")

    # Delete the converted file
    os.remove(output_file_path)

# Define the "/status" command handler
@app.on_message(filters.command("status"))
def status_command_handler(client: Client, message: Message):
    # Call the get_status_message function from the status.py file
    # to get the current status of file downloading and uploading
    status_msg = get_status_message()
    message.reply_text(status_msg)

# Start the Bot
app.run()
