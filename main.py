import os
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from status import convert_to_streamable_video


# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(level=logging.INFO)


# Create a Pyrogram client instance
app = Client(
    "my_bot",
    api_id=os.getenv("7068313"),
    api_hash=os.getenv("d7446aca34e84b8539a1a8817630d1b5"),
    bot_token=os.getenv("5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk")
)


# Handler for /start command
@app.on_message(filters.command("start"))
async def start_command_handler(client: Client, message: Message):
    await message.reply_text("Hi, send me a file and I'll convert it to a streamable video!")


# Handler for /convert command
@app.on_message(filters.command("convert"))
async def convert_command_handler(client: Client, message: Message):
    # Check if message has a reply and has a media
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("Reply to a media file to convert it to a streamable video!")
        return

    # Convert media to streamable video
    file_path = await message.reply_to_message.download()
    streamable_path = convert_to_streamable_video(file_path)
    if not streamable_path:
        await message.reply_text("Failed to convert the media to a streamable video!")
        return

    # Send the streamable video as a reply
    await message.reply_video(streamable_path)

    # Remove temporary files
    os.remove(file_path)
    os.remove(streamable_path)


# Run the client
app.run()
