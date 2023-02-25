import os
from pyrogram import Client, filters
from moviepy.editor import *

# Set your API credentials and bot token here
API_ID = 7068313
API_HASH = "d7446aca34e84b8539a1a8817630d1b5"
BOT_TOKEN = "5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hi! Send me any file and I'll convert it to video.")


@app.on_message(filters.document)
async def convert_to_video(client, message):
    # Download the file to the server
    file_path = await message.download()

    # Check if the file is already a video
    if any(file_path.endswith(ext) for ext in [".mp4", ".avi", ".mov", ".wmv"]):
        # Send the original file back to the user
        await client.send_document(chat_id=message.chat.id, document=file_path)
    else:
        # Convert the file to mp4 format
        video_path = os.path.splitext(file_path)[0] + ".mp4"
        video = VideoFileClip(file_path)
        video.write_videofile(video_path)

        # Send the converted file back to the user
        await client.send_video(chat_id=message.chat.id, video=video_path)

        # Remove the downloaded files from the server
        os.remove(file_path)
        os.remove(video_path)


if __name__ == "__main__":
    app.run()
