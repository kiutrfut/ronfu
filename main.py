import os
import logging
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from pyrogram.types import Message

from status import get_file_status, convert_to_streamable_video

# initialize logging
name = os.path.basename(file)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(name)

# initialize Pyrogram client
api_id = int(os.environ.get("7068313", 0))
api_hash = os.environ.get("d7446aca34e84b8539a1a8817630d1b5")
bot_token = os.environ.get("5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk")
if not api_id or not api_hash or not bot_token:
    logger.error("Missing environment variable(s) API_ID, API_HASH, or BOT_TOKEN.")
    quit()
app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


@app.on_message(filters.command("status"))
def status_command_handler(_, message: Message):
    try:
        file_path = message.reply_to_message.document.file_path
    except AttributeError:
        message.reply_text("Please reply to a file to get its status.")
        return
    except MessageEmpty:
        message.reply_text("The replied message is empty.")
        return

    status_msg = get_file_status(file_path)
    message.reply_text(status_msg)


@app.on_message(filters.command("convert"))
def convert_command_handler(_, message: Message):
    try:
        file_id = message.reply_to_message.document.file_id
        file_name = message.reply_to_message.document.file_name
    except AttributeError:
        message.reply_text("Please reply to a file to convert.")
        return
    except MessageEmpty:
        message.reply_text("The replied message is empty.")
        return

    file_path = app.download_media(file_id, file_name)
    try:
        streamable_path = convert_to_streamable_video(message.chat.id, file_id, file_name, file_path)
        message.reply_video(video=streamable_path)
    except Exception as e:
        logger.error(f"Failed to convert file: {e}")
        message.reply_text("Failed to convert file. Please try again later.")


if name == "main":
    app.run()
