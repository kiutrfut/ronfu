import os
import tempfile
import moviepy.editor as mp
from telegram.ext import CommandHandler, Updater

def vid(update, context):
    # get the file from the user
    file = context.bot.get_file(update.message.document.file_id)
    
    # create a temporary file to store the downloaded file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file.download(out=temp_file)
        filename = temp_file.name
    
    # convert the file to a video
    video_filename = convert_to_video(filename)
    
    # send the video file to the user
    with open(video_filename, "rb") as video_file:
        context.bot.send_video(chat_id=update.message.chat_id, video=video_file)
    
    # delete the temporary files
    os.remove(filename)
    os.remove(video_filename)

def convert_to_video(filename):
    # create a video file with the same name as the input file
    video_filename = os.path.splitext(filename)[0] + ".mp4"
    
    # load the input file using moviepy
    clip = mp.VideoFileClip(filename)
    
    # resize the clip to a reasonable size for video playback
    clip_resized = clip.resize(height=360)
    
    # write the video file using the libx264 codec
    clip_resized.write_videofile(video_filename, codec="libx264", audio_codec="aac")
    
    return video_filename

# set up the Telegram bot
updater = Updater(token="YOUR_BOT_TOKEN", use_context=True)
dispatcher = updater.dispatcher

# set up the /vid command handler
vid_handler = CommandHandler("vid", vid)
dispatcher.add_handler(vid_handler)

# start the bot
updater.start_polling()
