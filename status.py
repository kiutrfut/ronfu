import psutil

def get_status_message():
    # Get the current system memory usage
    memory_percent = psutil.virtual_memory().percent

    # Get the current system CPU usage
    cpu_percent = psutil.cpu_percent()

    # Create a status message
    status_message = f"CPU usage: {cpu_percent}%\nMemory usage: {memory_percent}%"

    return status_message
