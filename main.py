import os
from pyrogram import Client, filters
from moviepy.editor import *
from status import get_status_message

# Set your API credentials and bot token here
API_ID = 7068313
API_HASH = "d7446aca34e84b8539a1a8817630d1b5"
BOT_TOKEN = "5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# define global variable to store the current status message ID
status_message_id = None

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hi! Send me any file and I'll convert it to video.")

@app.on_message(filters.command("convert"))
async def convert_command(client, message):
    # Check if the message has a reply and if it is a document
    if message.reply_to_message and message.reply_to_message.document:
        # Download the file to the server
        file_path = await message.reply_to_message.download()

        # Check if the file is a video
        if not any(file_path.endswith(ext) for ext in [".mp4", ".avi", ".mov", ".wmv"]):
            # Convert the file to mp4 format
            video_path = os.path.splitext(file_path)[0] + ".mp4"
            video = VideoFileClip(file_path)
            video.write_videofile(video_path)

            # Send the converted file back to the user
            await client.send_video(chat_id=message.chat.id, video=video_path)

            # Remove the downloaded files from the server
            os.remove(file_path)
            os.remove(video_path)
        else:
            # Send the original file back to the user
            await client.send_document(chat_id=message.chat.id, document=file_path)

            # Remove the downloaded file from the server
            os.remove(file_path)
    else:
        await message.reply_text("Please reply to a document with /convert to convert it to video.")

@app.on_message(filters.command("status"))
async def get_status(client, message):
    global status_message_id
    status_message = get_status_message()
    if not status_message_id:
        # if the status message is not set yet, create a new message
        status_message_obj = await client.send_message(chat_id=message.chat.id, text=status_message)
        status_message_id = status_message_obj.message_id
    else:
        # if the status message is already set, edit the existing message
        await client.edit_message_text(chat_id=message.chat.id, message_id=status_message_id, text=status_message)

if __name__ == "__main__":
    app.run()
