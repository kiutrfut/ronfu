import telebot
import os

# Replace YOUR_TOKEN_HERE with your Telegram Bot API token
bot = telebot.TeleBot("5562112612:AAH7Sbz2iIAdoPknjv0FnuiNbiDa_5OFYQA")

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to the file converter bot! Type /help to see the available commands.")

# Help command
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "This bot can convert files to mp4 and document to video format. To use the bot, send a file and type /convert to convert the file to video format or /convert2 to convert the file to mp4 format. Type /status to check the status of your conversion.")

# Convert command
@bot.message_handler(commands=['convert'])
def convert(message):
    if message.reply_to_message is not None and message.reply_to_message.document is not None:
        file_info = bot.get_file(message.reply_to_message.document.file_id)
        file = bot.download_file(file_info.file_path)
        with open("input_file.txt", 'wb') as f:
            f.write(file)
        # Add your code to convert file to video format here
        bot.reply_to(message, "File converted to video format.")
    else:
        bot.reply_to(message, "Please reply to a document to convert it to video format.")

# Convert2 command
@bot.message_handler(commands=['convert2'])
def convert2(message):
    if message.reply_to_message is not None and message.reply_to_message.document is not None:
        file_info = bot.get_file(message.reply_to_message.document.file_id)
        file = bot.download_file(file_info.file_path)
        with open("input_file.txt", 'wb') as f:
            f.write(file)
        # Add your code to convert file to mp4 format here
        bot.reply_to(message, "File converted to mp4 format.")
    else:
        bot.reply_to(message, "Please reply to a document to convert it to mp4 format.")

# Status command
@bot.message_handler(commands=['status'])
def status(message):
    if os.path.isfile("input_file.txt"):
        bot.reply_to(message, "File downloaded and ready for conversion.")
    else:
        bot.reply_to(message, "No file has been downloaded for conversion yet.")

# Start the bot
bot.polling()
