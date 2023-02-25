import os
import subprocess

from pyrogram import Client, filters
from pyrogram.types import Message
from status import get_file_status, get_video_info, get_file_size, convert_to_streamable_video

app = Client("my_bot")

# Status command handler
@app.on_message(filters.command(["status"]))
def status_command_handler(client: Client, message: Message):
    if message.reply_to_message:
        file_id = message.reply_to_message.video.file_id
        status_msg = get_file_status(client, message.chat.id, file_id)
        message.reply_text(status_msg)
    else:
        message.reply_text("Please reply to a video file to get its status.")


# Convert command handler
@app.on_message(filters.command(["convert"]))
def convert_command_handler(client: Client, message: Message):
    if message.reply_to_message:
        # Get file info
        file_id = message.reply_to_message.video.file_id
        file_name = message.reply_to_message.video.file_name
        file_size = get_file_size(client, file_id)
        duration = get_video_info(client, file_id)

        # Send initial message
        initial_msg = f"Converting to streamable format...\n\n<b>File name:</b> {file_name}\n<b>File size:</b> {file_size}\n<b>Duration:</b> {duration}"
        message.reply_text(initial_msg, parse_mode="html")

        # Convert to streamable format
        streamable_path = convert_to_streamable_video(client, message.chat.id, file_id, file_name)

        # Upload streamable video
        message.reply_video(streamable_path, supports_streaming=True)

        # Clean up
        os.remove(streamable_path)
    else:
        message.reply_text("Please reply to a video file to convert it.")


app.run()
