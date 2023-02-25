import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from status import get_file_status, convert_to_streamable_video


# Get the environment variables
API_ID = int(os.environ.get("7068313"))
API_HASH = os.environ.get("d7446aca34e84b8539a1a8817630d1b5")
BOT_TOKEN = os.environ.get("5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk")

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

    status_msg = get_file_status(file_id)
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
    streamable_path = convert_to_streamable_video(chat_id, file_id, file_name, file_path)

    message.reply_video(video=streamable_path)


# Start the bot
if name == "main":
    app.run()
