import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from commands import start, help, convert2

load_dotenv()

TOKEN = os.getenv('5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk')

updater = Updater(TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('convert2', convert2))
updater.dispatcher.add_handler(MessageHandler(Filters.document.mime_type('application/pdf'), convert2))

updater.start_polling()
updater.idle()
