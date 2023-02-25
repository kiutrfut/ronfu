from pyrogram import Client, filters
from pyrogram.types import Message

# Create a dictionary to store the status of ongoing file downloads and uploads
status = {}

# Create a Pyrogram client instance
app = Client("my_bot")

# Define a command handler for the /start command
@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    await message.reply_text("Hello! Send me a file and I will upload it to Telegram.")

# Define a command handler for the /status command
@app.on_message(filters.command("status"))
async def status_handler(client: Client, message: Message):
    # Check if there are any ongoing file downloads or uploads
    if len(status) == 0:
        await message.reply_text("There are no ongoing file downloads or uploads.")
    else:
        # Iterate through the status dictionary and generate a status message
        status_message = "Current status:\n"
        for key, value in status.items():
            status_message += f"{key}: {value}\n"
        await message.reply_text(status_message)

# Define a handler for when a file is sent to the bot
@app.on_message(filters.document)
async def document_handler(client: Client, message: Message):
    # Get the file name and size
    file_name = message.document.file_name
    file_size = message.document.file_size

    # Add the file to the status dictionary with a status of "downloading"
    status[file_name] = "downloading"

    # Download the file to the local file system
    await message.download(file_name)

    # Update the status to "uploading"
    status[file_name] = "uploading"

    # Upload the file to Telegram
    await client.send_document(message.chat.id, file_name)

    # Remove the file from the status dictionary
    del status[file_name]

    # Send a message to the user indicating that the file has been uploaded
    await message.reply_text(f"{file_name} ({file_size} bytes) has been uploaded to Telegram.")

# Start the Pyrogram client
app.run()
