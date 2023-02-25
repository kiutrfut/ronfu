import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from status import get_file_status, get_video_info, get_file_size

app = Client("my_bot")

@app.on_message(filters.command(['start']))
def start_command_handler(client: Client, message: Message):
    client.send_message(chat_id=message.chat.id, text="Hi! Send me a video file and I will convert it to a streamable format.")

@app.on_message(filters.video)
def video_handler(client: Client, message: Message):
    file_id = message.video.file_id
    file_name = message.video.file_name
    chat_id = message.chat.id
    status_msg = client.send_message(chat_id, f"Processing {file_name}...")
    file_path = client.download_media(file_id, file_name=file_name)
    streamable_path = convert_to_streamable_video(chat_id, file_id, file_name, file_path)
    client.delete_messages(chat_id, status_msg.message_id)
    client.send_video(chat_id, streamable_path)

@app.on_message(filters.command(['status']))
def status_command_handler(client: Client, message: Message):
    file_id = message.reply_to_message.video.file_id
    chat_id = message.chat.id
    status_msg = client.send_message(chat_id, "Getting status...")
    file_status = get_file_status(client, chat_id, file_id)
    video_info = get_video_info(file_status)
    file_size = get_file_size(file_status)
    duration = video_info.get('duration')
    bitrate = video_info.get('bitrate')
    width = video_info.get('width')
    height = video_info.get('height')
    status_msg_text = f"File size: {file_size}\nDuration: {duration}s\nBitrate: {bitrate}\nResolution: {width}x{height}"
    client.edit_message_text(chat_id, status_msg.message_id, text=status_msg_text)

def convert_to_streamable_video(chat_id: int, file_id: str, file_name: str, file_path: str) -> str:
    streamable_file_name = file_name.split(".")[0] + "_streamable.mp4"
    streamable_path = f"{chat_id}_{file_id}_{streamable_file_name}"
    subprocess.run(["ffmpeg", "-i", file_path, "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "copy", streamable_path])
    return streamable_path

if name == 'main':
    app.run()
