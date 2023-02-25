import os
import subprocess

from pyrogram.errors import FilePartsInvalid, FileReferenceEmpty, FileIdInvalid
from pyrogram.types import Video, Message
from pyrogram import Client


def get_file_status(client: Client, chat_id: int, file_id: str) -> str:
    try:
        file_info = client.get_file_info(file_id)
        file_size = file_info.size
        file_name = file_info.file_name
        return f"File Name: {file_name}\nFile Size: {file_size} bytes"
    except (FilePartsInvalid, FileReferenceEmpty, FileIdInvalid):
        return "Failed to fetch file information."


def convert_to_streamable_video(client: Client, chat_id: int, file_id: str, file_name: str) -> bool:
    try:
        temp_path = os.path.join("temp", file_name)
        client.download_media(file_id, temp_path)

        # Generate output file name with mp4 extension
        output_file_name = os.path.splitext(file_name)[0] + ".mp4"
        output_path = os.path.join("temp", output_file_name)

        # Run ffmpeg command to convert file to streamable mp4 format
        cmd = f"ffmpeg -i {temp_path} -c:v libx264 -profile:v main -level 3.1 -preset medium -crf 23 -c:a aac -b:a 128k -movflags +faststart {output_path}"
        subprocess.run(cmd, shell=True, check=True)

        # Upload converted video file to Telegram as video message
        client.send_video(
            chat_id=chat_id,
            video=output_path,
            caption="Converted video",
            supports_streaming=True
        )

        return True
    except Exception as e:
        print(e)
        return False


def convert_command_handler(client: Client, message: Message):
    # Check if message has reply
    if message.reply_to_message is None:
        message.reply_text("Please reply to a video message to convert.")
        return

    # Check if the replied message is a video
    if message.reply_to_message.video is None:
        message.reply_text("Please reply to a video message to convert.")
        return

    # Get file ID and file name
    file_id = message.reply_to_message.video.file_id
    file_name = message.reply_to_message.video.file_name

    # Check if file is already in streamable format
    if file_name.endswith(".mp4"):
        message.reply_text("This video is already in streamable format.")
        return

    # Convert video to streamable format
    message.reply_text("Converting video...")
    success = convert_to_streamable_video(client, message.chat.id, file_id, file_name)

    if success:
        message.reply_text("Video converted successfully!")
    else:
        message.reply_text("Failed to convert video.")


api_id = os.environ.get("7068313")
api_hash = os.environ.get("d7446aca34e84b8539a1a8817630d1b5")
bot_token = os.environ.get("5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk")

if api_id is None:
    api_id = input("Enter API ID: ").strip()

if api_hash is None:
    api_hash = input("Enter API hash: ").strip()

if bot_token is None:
    bot_token = input("Enter bot token: ").strip()

app = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

app.run(
    # Start command handlers
    {
        "convert": convert_command_handler
    }
)
