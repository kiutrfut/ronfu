import os

from pyrogram import Client
from pyrogram.types import Message
from hurry.filesize import size
from humanfriendly import format_timespan


async def get_file_status(client: Client, chat_id: int, file_id: str) -> str:
    message = await client.send_message(chat_id, f"Checking status for file ID: {file_id}...")
    file_info = await client.get_file_info(file_id)
    file_size = file_info.size
    local_file_path = f"./downloads/{file_id}"
    if os.path.exists(local_file_path):
        local_file_size = os.path.getsize(local_file_path)
        download_progress = int((local_file_size / file_size) * 100)
        download_speed = size(file_size / file_info.duration)
        download_eta = format_timespan((file_size - local_file_size) / file_info.avg_download_speed)
        status = f"Download Status:\nProgress: {download_progress}%\nSpeed: {download_speed}/s\nETA: {download_eta}"
        await message.edit(status)
    else:
        status = "Download Status: Not Started Yet"
        await message.edit(status)
    return status


async def convert_to_streamable_video(client: Client, chat_id: int, file_id: str, file_name: str, file_path: str) -> str:
    message = await client.send_message(chat_id, f"Converting to streamable format...")
    streamable_file_path = f"./streamable/{file_name}"
    if os.path.exists(streamable_file_path):
        os.remove(streamable_file_path)
    conversion_command = [
        "ffmpeg",
        "-i", file_path,
        "-preset", "ultrafast",
        "-c:a", "copy",
        "-c:v", "libx264",
        "-crf", "23",
        "-maxrate", "1M",
        "-bufsize", "2M",
        "-vf", "scale='if(gt(a,16/9),1280,-2)':'if(gt(a,16/9),-2,720)',format=yuv420p",
        "-movflags", "faststart",
        streamable_file_path
    ]
    process = await asyncio.create_subprocess_exec(*conversion_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    while True:
        output = await process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            await message.edit(f"Converting to streamable format...\n
{output.decode().strip()}
")
    await message.edit("Conversion completed successfully!")
    return streamable_file_path
