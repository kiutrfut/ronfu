import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from status import get_file_status, convert_to_streamable_video

# Enable logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
API_ID = int(os.environ.get("7068313"))
API_HASH = os.environ.get("d7446aca34e84b8539a1a8817630d1b5")
BOT_TOKEN = os.environ.get("5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk")

# Create a Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Handler function for /start command
@app.on_message(filters.command("start"))
async def start_command_handler(client: Client, message: Message):
    await message.reply_text("Hi there! Send me any file and I'll tell you if it's streamable.")


# Handler function for /status command
@app.on_message(filters.command("status"))
async def status_command_handler(client: Client, message: Message):
    # Check if a file is attached
    if not message.document:
        await message.reply_text("Please attach a file.")
        return

    # Get file status
    file_id = message.document.file_id
    file_name = message.document.file_name
    file_status = get_file_status(file_id)

    # Reply with file status
    if file_status:
        await message.reply_text(f"{file_name} is streamable.")
    else:
        await message.reply_text(f"{file_name} is not streamable.")


# Handler function for /convert command
@app.on_message(filters.command("convert"))
async def convert_command_handler(client: Client, message: Message):
    # Check if a file is attached
    if not message.document:
        await message.reply_text("Please attach a file.")
        return

    # Download the file
    file_id = message.document.file_id
    file_name = message.document.file_name
    file_path = await client.download_media(message=message)

    # Convert to streamable format
    streamable_path = convert_to_streamable_video(message.chat.id, file_id, file_name, file_path)

    # Reply with the streamable video
    if streamable_path:
        await client.send_video(
            chat_id=message.chat.id,
            video=streamable_path,
            reply_to_message_id=message.message_id,
            caption=f"{file_name} is now streamable.",
        )
    else:
        await message.reply_text(f"{file_name} cannot be converted to streamable format.")


# Run the client
app.run()
