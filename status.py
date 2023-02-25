import os
from pyrogram import Client
from hurry.filesize import size
import subprocess


async def get_file_status(client: Client, chat_id: int, file_id: str) -> str:
    try:
        file_info = await client.get_file_info(file_id)
        file_size = get_file_size(file_info.file_size)
        status_msg = f"File name: {file_info.file_name}\nFile size: {file_size}"
        if file_info.is_audio:
            status_msg += "\n\n<b>Cannot convert audio files to streamable format!</b>"
        elif file_info.is_video:
            status_msg += "\n\nUse /convert command to convert to streamable format."
        else:
            status_msg += "\n\n<b>This type of file cannot be converted to streamable format!</b>"
        return status_msg
    except Exception as e:
        print(e)
        return "An error occurred while fetching file information!"


async def get_video_info(file_path: str) -> dict:
    try:
        result = subprocess.check_output(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file_path])
        video_info = eval(result.decode('utf-8'))
        return video_info
    except Exception as e:
        print(e)
        return {}


def get_file_size(file_size_bytes: int) -> str:
    return size(file_size_bytes)


async def convert_to_streamable_video(chat_id: int, file_id: str, file_name: str, file_path: str) -> str:
    try:
        duration = subprocess.check_output(['ffprobe', '-i', file_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")])
        duration = int(float(duration))
    except:
        duration = 0
    
    streamable_file_path = os.path.join("downloads", f"{file_id}.mp4")
    if os.path.exists(streamable_file_path):
        os.remove(streamable_file_path)
    
    command = ['ffmpeg', '-i', file_path, '-c', 'copy', '-movflags', '+faststart', '-hide_banner', '-loglevel', 'error', '-nostats', '-f', 'mp4', '-y', streamable_file_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print(output.strip())
    return streamable_file_path
