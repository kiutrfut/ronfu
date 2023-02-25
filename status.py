import os
import psutil

from datetime import datetime
from hurry.filesize import size


class DownloadStatus:
    def init(self, file_size):
        self.file_size = file_size
        self.start_time = datetime.now()
        self.downloaded_bytes = 0

    def update(self, chunk):
        self.downloaded_bytes += len(chunk)

    def get_speed(self):
        elapsed_time = (datetime.now() - self.start_time).seconds
        return self.downloaded_bytes / elapsed_time

    def get_eta(self):
        bytes_left = self.file_size - self.downloaded_bytes
        seconds_left = bytes_left / self.get_speed()
        return str(datetime.now() + timedelta(seconds=seconds_left)).split(".")[0]

    def get_progress(self):
        progress = self.downloaded_bytes / self.file_size
        return round(progress * 100)


class UploadStatus:
    def init(self, file_size):
        self.file_size = file_size
        self.start_time = datetime.now()
        self.uploaded_bytes = 0

    def update(self, current, total):
        self.uploaded_bytes = current

    def get_speed(self):
        elapsed_time = (datetime.now() - self.start_time).seconds
        return self.uploaded_bytes / elapsed_time

    def get_eta(self):
        bytes_left = self.file_size - self.uploaded_bytes
        seconds_left = bytes_left / self.get_speed()
        return str(datetime.now() + timedelta(seconds=seconds_left)).split(".")[0]

    def get_progress(self):
        progress = self.uploaded_bytes / self.file_size
        return round(progress * 100)


def status():
    process = psutil.Process(os.getpid())
    memory_used = process.memory_info().rss / 1024 ** 2
    disk_used = psutil.disk_usage("/").percent
    cpu_usage = psutil.cpu_percent()

    download_status = app.get_download_status()
    upload_status = app.get_upload_status()

    message = f"Memory used: {memory_used:.2f} MB\nDisk used: {disk_used}%\nCPU usage: {cpu_usage}%\n\n"
    if download_status:
        message += f"Downloading {download_status.name} ({size(download_status.size)})\n"
        message += f"Progress: {download_status.progress}%\n"
        message += f"Downloaded: {size(download_status.downloaded_bytes)} of {size(download_status.size)}\n"
        message += f"Speed: {size(download_status.speed)}/s\n"
        message += f"ETA: {download_status.eta}\n\n"
    if upload_status:
        message += f"Uploading {upload_status.name} ({size(upload_status.size)})\n"
        message += f"Progress: {upload_status.progress}%\n"
        message += f"Uploaded: {size(upload_status.uploaded_bytes)} of {size(upload_status.size)}\n"
        message += f"Speed: {size(upload_status.speed)}/s\n"
        message += f"ETA: {upload_status.eta}"

    return message
