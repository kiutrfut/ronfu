import telebot

# Replace YOUR_TOKEN_HERE with your Telegram Bot API token
bot = telebot.TeleBot("5562112612:AAH7Sbz2iIAdoPknjv0FnuiNbiDa_5OFYQA")

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to the file converter bot! Type /help to see the available commands.")

# Help command
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "This bot can convert files to mp4 and document to video format. Type /convert to convert file to video format and /convert2 to convert file to mp4 format.")

# Convert command
@bot.message_handler(commands=['convert'])
def convert(message):
    # Add your code to convert file to video format here
    bot.reply_to(message, "File converted to video format.")

# Convert2 command
@bot.message_handler(commands=['convert2'])
def convert2(message):
    # Add your code to convert file to mp4 format here
    bot.reply_to(message, "File converted to mp4 format.")

# Start the bot
bot.polling()
