import sys
import os
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.raw.types import InputFile
from pyrogram.types import Message
import time
import telebot
from command2 import convert2  # import the convert2 command

# Replace YOUR_TOKEN_HERE with your Telegram Bot API token
bot = telebot.TeleBot("5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk")

# Replace with your API_ID and API_HASH
api_id = 7068313
api_hash = "d7446aca34e84b8539a1a8817630d1b5"
app = Client("my_account", api_id=api_id, api_hash=api_hash)


# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to the file converter bot! Type /help to see the available commands.")


# Help command
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "This bot can convert files to mp4 and documents to video format. Type /convert to convert file to video format and /convert2 to convert document to mp4 format.")


# Convert command
@bot.message_handler(commands=['convert'])
def convert(message):
    if message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document
        if document.mime_type.startswith('video/'):
            bot.reply_to(message, "File is already a video.")
        else:
            try:
                # Download the file using pyrogram
                with app:
                    downloaded_file = app.download_media(message.reply_to_message)
                # Convert the file using ffmpeg
                os.system(f"ffmpeg -i {downloaded_file} -preset veryfast -movflags +faststart -c:v libx264 -c:a aac -b:a 192k -vf scale=w=720:h=-1:force_original_aspect_ratio=decrease {downloaded_file}.mp4")
                # Upload the converted file using pyrogram
                with app:
                    app.send_video(message.chat.id, InputFile(f"{downloaded_file}.mp4"))
                bot.reply_to(message, "File converted to video format.")
                os.remove(downloaded_file)
                os.remove(f"{downloaded_file}.mp4")
            except FloodWait as e:
                time.sleep(e.x)
            except Exception as e:
                bot.reply_to(message, f"Error converting file: {e}")
    else:
        bot.reply_to(message, "Please reply to a document to convert it to video format.")


# Convert2 command
@bot.message_handler(commands=['convert2'])
def handle_convert2(message):
    convert2(bot, message)


if name == 'main':
    bot.polling()
