import os
import time
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from hurry.filesize import size
import subprocess

# Create a new Telegram Bot using the Bot Father and get the API token
API_TOKEN = "5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk"

# Create a new Pyrogram client instance
app = Client("my_bot", api_id=7068313, api_hash="d7446aca34e84b8539a1a8817630d1b5", bot_token=API_TOKEN)

# Define the "/start" command handler
@app.on_message(filters.command("start"))
def start_command_handler(client: Client, message: Message):
    # Send a welcome message to the user
    message.reply_text("Hello! I'm a Telegram Bot.")

# Define the "/convert" command handler
@app.on_message(filters.command("convert"))
def convert_command_handler(client: Client, message: Message):
    # Check if a video file is attached to the message
    if not message.document or message.document.mime_type.split('/')[0] != 'video':
        message.reply_text("Please upload a video file.")
        return
    
    # Download the video file to the server
    file_name = message.document.file_name
    file_size = message.document.file_size
    message.reply_text(f"Downloading {file_name} ({size(file_size)})...")
    start_time = time.time()
    video_path = client.download_media(message=message, file_name="video.mp4")
    download_time = round(time.time() - start_time)
    message.reply_text(f"Download complete! ({download_time} seconds)")
    
    # Convert the video file to mpegts format
    message.reply_text(f"Converting {file_name}...")
    start_time = time.time()
    output_file_name = os.path.splitext(file_name)[0] + ".ts"
    subprocess.run(['ffmpeg', '-i', video_path, '-codec', 'copy', '-bsf:v', 'h264_mp4toannexb', '-map', '0', '-f', 'mpegts', output_file_name])
    convert_time = round(time.time() - start_time)
    message.reply_text(f"Conversion complete! ({convert_time} seconds)")
    
    # Send the converted video file to the user
    message.reply_text(f"Sending {output_file_name}...")
    start_time = time.time()
    with open(output_file_name, "rb") as file:
        app.send_video(message.chat.id, video=file, caption=output_file_name)
    upload_time = round(time.time() - start_time)
    message.reply_text(f"Upload complete! ({upload_time} seconds)")
    os.remove(output_file_name)

# Define the "/status" command handler
@app.on_message(filters.command("status"))
def status_command_handler(client: Client, message: Message):
    # Get the disk usage statistics for the server
    disk_usage = subprocess.check_output(['df', '-h']).decode('utf-8')
    message.reply_text(f"Disk Usage:\n{disk_usage}")

# Start the Bot
app.run()
