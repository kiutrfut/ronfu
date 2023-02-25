from pyrogram import Client, filters
from pyrogram.types import Message
from status import status

# Create a new Telegram Bot using the Bot Father and get the API token
API_TOKEN = "5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk"

# Create a new Pyrogram client instance
app = Client("my_bot", api_id=7068313, api_hash="d7446aca34e84b8539a1a8817630d1b5", bot_token=API_TOKEN)

# Define the "/start" command handler
@app.on_message(filters.command("start"))
def start_command_handler(client: Client, message: Message):
    # Send a welcome message to the user
    message.reply_text("Hello! I'm a Telegram Bot.")

# Define the "/status" command handler
@app.on_message(filters.command("status"))
def status_command_handler(client: Client, message: Message):
    # Call the status function from the status.py file
    # to get the current status of file downloading and uploading
    current_status = status()
    # Send the current status as a message to the user
    message.reply_text(current_status)

# Start the Bot
app.run()
