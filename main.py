import subprocess
from pyrogram import types
import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from status import get_file_status, convert_to_streamable_video


# Get the environment variables
API_ID = int(os.environ.get("API_ID", 7068313))
API_HASH = os.environ.get("API_HASH", "d7446aca34e84b8539a1a8817630d1b5")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk")

if API_ID == 0 or not API_HASH or not BOT_TOKEN:
    print("Please provide API_ID, API_HASH and BOT_TOKEN as environment variables.")
    quit()

# Create the Client and connect to Telegram
app = Client("ronfu_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RonfuBot")


# Define the /start command handler
@app.on_message(filters.command(["start"]))
def start_command_handler(_, message: Message) -> None:
    message.reply_text("Hi, send me a file and I will tell you its details!")


# Define the /status command handler
@app.on_message(filters.command(["status"]))
def status_command_handler(_, message: Message) -> None:
    file_id = message.reply_to_message.document.file_id if message.reply_to_message else None
    if not file_id:
        message.reply_text("Please reply to a file to get its status.")
        return

    status_msg = get_file_status(app, message.chat.id, file_id)
    message.reply_text(status_msg)


# Define the /convert command handler
@app.on_message(filters.command(["convert"]))
def convert_command_handler(_, message: Message) -> None:
    file_id = message.reply_to_message.document.file_id if message.reply_to_message else None
    if not file_id:
        message.reply_text("Please reply to a file to convert it.")
        return

    file_name = message.reply_to_message.document.file_name
    chat_id = message.chat.id
    file_path = app.download_media(file_id)
    streamable_path = convert_to_streamable_video(app, chat_id, file_id, file_name)

    message.reply_video(video=streamable_path)

def convert_to_streamable_video(chat_id: int, file_id: str, file_name: str, file_path: str) -> str:
    # Use ffprobe to get the video duration
    duration = subprocess.check_output(['ffprobe', '-i', file_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")])
    duration = int(float(duration))

    # Set the output file name and path
    streamable_file_name = f"{file_name}_streamable.mp4"
    streamable_file_path = f"streamable/{chat_id}/{file_id}/{streamable_file_name}"

    # Create the streamable directory if it doesn't exist
    os.makedirs(os.path.dirname(streamable_file_path), exist_ok=True)

    # Convert the video to a streamable format using ffmpeg
    subprocess.run(['ffmpeg', '-y', '-i', file_path, '-c:v', 'libx264', '-preset', 'fast', '-profile:v', 'baseline', '-level', '3.0', '-c:a', 'aac', '-movflags', '+faststart', '-vf', f"scale=w=trunc(oh*a/2)*2:h=720,setsar=1:1,drawtext=fontfile=OpenSans-Bold.ttf:text='%{{pts\:gmtime\:{duration}\:%H\\\\\:%M\\\\\:%S}}':x=(w-tw-10):y=(h-th-10):fontsize=30:fontcolor=white:box=1:boxcolor=black@0.5", streamable_file_path])

    return streamable_file_path    

# Start the bot
if __name__ == "__main__":
    app.run()
