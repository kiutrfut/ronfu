import os
import telegram
import subprocess

TOKEN = '5959482663:AAGnBMV2Rbrtr5k01AxYXrw-bRSJ9mIEjwk'
bot = telegram.Bot(token=TOKEN)

def convert_to_video(file_path):
    """
    Converts the given file to video format.
    Returns the path of the converted file.
    """
    video_path = file_path.split('.')[0] + '.mp4'
    subprocess.run(['ffmpeg', '-i', file_path, video_path])
    return video_path

def handle_start(update, context):
    """
    Handles the /start command.
    Sends a welcome message to the user.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the File Converter Bot! Send me a document file and use the /vid or /mp4 command to convert it to a video or mp4 file, respectively.")

def handle_help(update, context):
    """
    Handles the /help command.
    Sends a help message to the user.
    """
    help_message = "This bot can convert any document to a video or mp4 file. Here are the available commands:\n\n"
    help_message += "/start - Get a welcome message\n"
    help_message += "/help - Get help with using the bot\n"
    help_message += "/vid - Convert a document file to a video file\n"
    help_message += "/mp4 - Convert any file to mp4 format\n"
    help_message += "/status - Check the current status of the bot\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

def handle_vid(update, context):
    """
    Handles the /vid command.
    Converts the document file sent by the user to video format and sends it back.
    """
    file = update.message.document
    file_path = bot.get_file(file.file_id).download()
    video_path = convert_to_video(file_path)
    context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, 'rb'))
    os.remove(file_path)
    os.remove(video_path)

def handle_mp4(update, context):
    """
    Handles the /mp4 command.
    Converts the file sent by the user to mp4 format and sends it back.
    """
    file = update.message.document or update.message.video or update.message.audio or update.message.voice or update.message.video_note or update.message.animation or update.message.photo[-1]
    file_path = bot.get_file(file.file_id).download()
    mp4_path = convert_to_mp4(file_path)
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(mp4_path, 'rb'))
    os.remove(file_path)
    os.remove(mp4_path)

def handle_status(update, context):
    """
    Handles the /status command.
    Sends a status message to the user.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm alive and ready to convert your files!")

def convert_to_mp4(file_path):
    """
    Converts the given file to mp4 format.
    Returns the path of the converted file.
    """
    mp4_path = file_path.split('.')[0] + '.mp4'
    subprocess.run(['ffmpeg', '-i', file_path, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-b:a', '128k', '-ac', '2', '-y', mp4_path])
    return mp4_path

if name == 'main':
    updater = telegram.ext.Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(telegram.ext.CommandHandler('start', handle_start))
    dp.add_handler(telegram.ext.CommandHandler('help', handle_help))
    dp.add_handler(telegram.ext.CommandHandler('vid', handle_vid))
    dp.add_handler(telegram.ext.CommandHandler('mp4', handle_mp4))
    dp.add_handler(telegram.ext.CommandHandler('status', handle_status))

    updater.start_polling()
    updater.idle()
