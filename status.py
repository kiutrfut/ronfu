import os
import ffmpeg
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import MessageNotModified

app = Client("my_account")


@app.on_message(filters.command(["status"]))
async def status_command_handler(client: Client, message: Message):
    chat_id = message.chat.id
    video_file_path = f"{chat_id}.mp4"
    if os.path.exists(video_file_path):
        video_duration = await get_video_duration(video_file_path)
        status_msg = f"Your video is still being processed! Please wait for {video_duration} minutes!"
    else:
        status_msg = "No video is being processed at the moment."
    try:
        await message.reply_text(status_msg)
    except MessageNotModified:
        pass


@app.on_message(filters.command(["convert"]))
async def convert_command_handler(client: Client, message: Message):
    chat_id = message.chat.id
    replied_msg = message.reply_to_message
    if replied_msg is None:
        await message.reply_text("Please reply to a video file to convert.")
        return
    elif replied_msg.video is None:
        await message.reply_text("Please reply to a video file to convert.")
        return
    else:
        input_file_path = f"{chat_id}.{replied_msg.video.file_name.split('.')[-1]}"
        await replied_msg.download(input_file_path)
        await message.reply_text("Your video is being processed. Please wait...")
        await convert_to_streamable_video(input_file_path, chat_id)
        await message.reply_video(video=video_file_path)


async def convert_to_streamable_video(input_file_path: str, chat_id: int):
    (
        ffmpeg
        .input(input_file_path)
        .output(f"{chat_id}.mp4", pix_fmt="yuv420p", preset="ultrafast", tune="film", video_bitrate=5000, audio_codec="aac", audio_bitrate="192k")
        .run(overwrite_output=True)
    )
    os.remove(input_file_path)


async def get_video_duration(video_file_path: str) -> int:
    probe = ffmpeg.probe(video_file_path)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    duration = int(float(video_info['duration']))
    return duration
