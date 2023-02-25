import time
import datetime
from pyrogram import Client
from pyrogram.types import Message


async def get_file_status(client: Client, chat_id: int, file_id: str) -> str:
    file_info = await client.get_file_info(file_id)
    file_size = file_info.size
    file_name = file_info.file_name
    file_download_progress = 0
    file_upload_progress = 0

    # Get download progress
    if file_info.is_remote:
        while file_download_progress < 100:
            file_info = await client.get_file_info(file_id)
            file_download_progress = file_info.download_progress
            time.sleep(1)

    # Get upload progress
    message = await client.send_message(chat_id, f"Uploading {file_name}...")
    start_time = time.monotonic()
    async for status in client.iter_upload_progress(file_id):
        file_upload_progress = round(status * 100)
        elapsed_time = time.monotonic() - start_time
        estimated_total_time = datetime.timedelta(seconds=(elapsed_time / status) - elapsed_time)
        await message.edit_text(f"Uploading {file_name}... {file_upload_progress}%\n"
                                f"Elapsed time: {datetime.timedelta(seconds=elapsed_time)}\n"
                                f"Estimated total time: {estimated_total_time}")

    return f"{file_name}\nSize: {file_size}\nDownload progress: 100%\nUpload progress: {file_upload_progress}%"
