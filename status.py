import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class DownloadStatus:
    def init(self, file_size):
        self.file_size = file_size
        self.total_downloaded = 0
        self.start_time = time.time()
        
    def update(self, bytes_amount):
        self.total_downloaded += bytes_amount
    
    def get_progress_percentage(self):
        return round(self.total_downloaded / self.file_size * 100, 2)
    
    def get_elapsed_time(self):
        return time.time() - self.start_time
    
    def get_speed(self):
        elapsed_time = self.get_elapsed_time()
        speed = self.total_downloaded / elapsed_time
        return speed if elapsed_time > 0 else 0
    
    def get_remaining_time(self):
        remaining_bytes = self.file_size - self.total_downloaded
        remaining_time = remaining_bytes / self.get_speed() if self.get_speed() > 0 else 0
        return remaining_time


class UploadStatus:
    def init(self, file_size):
        self.file_size = file_size
        self.total_uploaded = 0
        self.start_time = time.time()
        
    def update(self, bytes_amount):
        self.total_uploaded += bytes_amount
    
    def get_progress_percentage(self):
        return round(self.total_uploaded / self.file_size * 100, 2)
    
    def get_elapsed_time(self):
        return time.time() - self.start_time
    
    def get_speed(self):
        elapsed_time = self.get_elapsed_time()
        speed = self.total_uploaded / elapsed_time
        return speed if elapsed_time > 0 else 0
    
    def get_remaining_time(self):
        remaining_bytes = self.file_size - self.total_uploaded
        remaining_time = remaining_bytes / self.get_speed() if self.get_speed() > 0 else 0
        return remaining_time


def get_status_message(download_status=None, upload_status=None):
    message = ""
    
    if download_status is not None:
        message += f"Download Status:\n"
        message += f"Progress: {download_status.get_progress_percentage()}%\n"
        message += f"Downloaded: {size(download_status.total_downloaded)}\n"
        message += f"Total Size: {size(download_status.file_size)}\n"
        message += f"Speed: {size(download_status.get_speed())}/s\n"
        message += f"Elapsed Time: {time.strftime('%H:%M:%S', time.gmtime(download_status.get_elapsed_time()))}\n"
        message += f"Remaining Time: {time.strftime('%H:%M:%S', time.gmtime(download_status.get_remaining_time()))}\n\n"
    
    if upload_status is not None:
        message += f"Upload Status:\n"
        message += f"Progress: {upload_status.get_progress_percentage()}%\n"
        message += f"Uploaded: {size(upload_status.total_uploaded)}\n"
        message += f"Total Size: {size(upload_status.file_size)}\n"
        message += f"Speed: {size(upload_status.get_speed())}/s\n"
        message += f"Elapsed Time: {time.strftime('%H:%M:%S', time.gmtime(upload_status.get_elapsed_time()))}\n"
        message += f"Remaining Time: {time.strftime('%H:%M:%S', time.gmtime(upload_status.get_remaining_time()))}\n\n"
    
    return message

def get_progress_bar_message(download_status=None, upload_status=None):
    if download_status is not None:
        progress = int(download_status.get_progress_percentage() / 2)
        progress_bar = "#" * progress + "-" * (50 - progress)
        return f"Progress: {download_status.get_progress_percentage()}%\n[{progress_bar}]"
    elif upload_status is not None:
        progress = int(upload_status.get_progress_percentage() / 2)
        progress_bar = "#" * progress + "-" * (50 - progress)
        return f"Progress: {upload_status.get_progress_percentage()}%\n[{progress_bar}]"
    else:
        return ""
