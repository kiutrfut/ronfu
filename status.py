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
