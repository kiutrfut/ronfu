from pyrogram import Client, filters
from pyrogram.types import Message
import time
import os

app = Client("my_bot")

async def progress(current, total, message: Message, text):
    """Displays the download progress bar."""
    chat_id = message.chat.id
    percent = (current * 100) // total
    status = "downloading" if text == "Download" else "uploading"
    speed = await app.get_readable_file_size(current / (time.time() - progress.start))
    message_text = (
        f"<b>{status}:</b> {percent}%\n"
        f"<b>Progress:</b> {'█' * percent}{''}\n"
        f"<b>Speed:</b> {speed}/s"
    )
    await app.edit_message_text(chat_id=chat_id, text=message_text, message_id=message.message_id)

progress.start = time.time()

@app.on_message(filters.command("status"))
async def status_command(client, message):
    """Displays the status of the ongoing operation."""
    chat_id = message.chat.id
    message_id = message.message_id
    status_message = await app.send_message(chat_id=chat_id, text="No active operation.")

    # Check if there is an ongoing download or upload task
    if "download" in app.storage:
        download = app.storage["download"]
        message_text = (
            f"<b>Downloading:</b> {download['file_name']}\n"
            f"<b>Progress:</b> {download['progress']}%\n"
            f"<b>Speed:</b> {download['speed']}\n"
        )
        await app.edit_message_text(chat_id=chat_id, text=message_text, message_id=status_message.message_id)

    elif "upload" in app.storage:
        upload = app.storage["upload"]
        message_text = (
            f"<b>Uploading:</b> {upload['file_name']}\n"
            f"<b>Progress:</b> {upload['progress']}%\n"
            f"<b>Speed:</b> {upload['speed']}\n"
        )
        await app.edit_message_text(chat_id=chat_id, text=message_text, message_id=status_message.message_id)

    else:
        await app.edit_message_text(chat_id=chat_id, text="No active operation.", message_id=status_message.message_id)


@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hi! Send me any file and I'll convert it to video.")


@app.on_message(filters.document)
async def convert_to_video(client, message):
    # Download the file to the server
    file_path = await message.download()

    # Set the storage variable to keep track of the download
    app.storage["download"] = {
        "file_name": message.document.file_name,
        "progress": 0,
        "speed": ""
    }

    # Send a message to indicate that the download has started
    status_message = await client.send_message(chat_id=message.chat.id, text="Downloading...")

    # Download the file and display the progress
    start = time.time()
    await client.download_media(
        message=message,
        file_name=file_path,
        progress=progress,
        progress_args=(status_message, "Download"),
        progress_kwargs=None
    )
    end = time.time()

    # Calculate the time taken to download the file and its size
    size = os.path.getsize(file_path)
    duration = round(end - start, 2)
    size = size / 1024 / 1024
    size = round(size, 2)

   
    # Set the storage variable to keep track of the upload
    app.storage["upload"] = {
        "file_name": message.document.file_name,
        "progress": 0,
        "speed": ""
    }

    # Send a message to indicate that the upload has started
    status_message = await client.send_message(chat_id=message.chat.id, text="Converting to video...")

    # Set the output file name and path
    output_file_name = os.path.splitext(file_path)[0] + ".mp4"
    
    # Convert the file to video format and display the progress
    start = time.time()
    os.system(f"ffmpeg -i {file_path} -preset veryfast -movflags +faststart -c:v libx264 -c:a aac -b:a 192k -threads 0 -strict experimental -f mp4 {output_file_name}")
    end = time.time()
    
    # Calculate the time taken to convert the file and its size
    size = os.path.getsize(output_file_name)
    duration = round(end - start, 2)
    size = size / 1024 / 1024
    size = round(size, 2)

    # Upload the converted file and display the progress
    app.storage["upload"]["progress"] = 0
    progress.start = time.time()
    await client.send_chat_action(chat_id=message.chat.id, action="upload_video")
    await client.send_video(
        chat_id=message.chat.id,
        video=output_file_name,
        duration=int(duration),
        width=1920,
        height=1080,
        caption=f"<b>File Name:</b> {message.document.file_name}\n"
                f"<b>Size:</b> {size} MB\n"
                f"<b>Time Taken:</b> {duration} seconds",
        progress=progress,
        progress_args=(status_message, "Upload"),
        progress_kwargs=None
    )

    # Remove the temporary files
    os.remove(file_path)
    os.remove(output_file_name)

    # Clear the storage variables
    app.storage.pop("download", None)
    app.storage.pop("upload", None)
