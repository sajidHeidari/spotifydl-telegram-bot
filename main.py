import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Import all other modules
try:
    from config.settings import TELEGRAM_TOKEN, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
    from bot_logic.keyboards import main_menu_keyboard
    from bot_logic.spotify_handler import get_playlist_tracks, download_audio
except (ValueError, ImportError) as e:
    # Use logging for critical errors on startup
    logging.critical(f"CRITICAL ERROR: {str(e)}. Bot cannot start.")
    # Exit if essential modules/configs are missing
    exit()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Command & Message Handlers ---

def start(update: Update, context: CallbackContext):
    """Handles the /start command."""
    user = update.effective_user
    update.message.reply_text(
        f"سلام {user.first_name} عزیز! به ربات دانلودر اسپاتیفای خوش آمدید.",
        reply_markup=main_menu_keyboard
    )

def help_command(update: Update, context: CallbackContext):
    """Handles the 'Help' button."""
    update.message.reply_text("کافیست روی دکمه 'دانلود از اسپاتیفای' کلیک کرده و سپس لینک پلی‌لیست مورد نظر خود را ارسال کنید.")

def handle_download_request(update: Update, context: CallbackContext):
    """Prompts the user for the playlist link."""
    update.message.reply_text("بسیار خب! لینک پلی‌لیست اسپاتیفای را برای من ارسال کنید:")

def handle_playlist_link(update: Update, context: CallbackContext):
    """Orchestrates the entire download process."""
    playlist_link = update.message.text
    chat_id = update.effective_chat.id
    
    context.bot.send_message(chat_id, "لینک دریافت شد. در حال استخراج لیست آهنگ‌ها...")
    
    tracks = get_playlist_tracks(playlist_link, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    
    if not tracks:
        context.bot.send_message(chat_id, "خطا! نتوانستم آهنگ‌های این پلی‌لیست را استخراج کنم. لطفاً از عمومی بودن پلی‌لیست و صحیح بودن لینک مطمئن شوید.")
        return

    context.bot.send_message(chat_id, f"✅ پلی‌لیست شما شامل {len(tracks)} آهنگ است. شروع دانلود و ارسال...")
    
    for i, track_name in enumerate(tracks, 1):
        context.bot.send_message(chat_id, f"({i}/{len(tracks)}) ⏳ در حال دانلود: {track_name}")
        
        audio_filepath = download_audio(track_name)
        
        if audio_filepath:
            try:
                with open(audio_filepath, 'rb') as audio_file:
                    context.bot.send_audio(chat_id=chat_id, audio=audio_file, title=os.path.basename(audio_filepath))
            except Exception as e:
                logger.error(f"Failed to send {track_name}. Error: {e}")
                context.bot.send_message(chat_id, f"❌ خطا در ارسال آهنگ: {track_name}")
            finally:
                os.remove(audio_filepath)
        else:
            context.bot.send_message(chat_id, f"⚠️ متاسفانه نتوانستم آهنگ '{track_name}' را پیدا یا دانلود کنم.")
            
    context.bot.send_message(chat_id, "🎉 تمام شد! همه آهنگ‌ها ارسال شدند.")


def main():
    """Starts and runs the bot."""
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Register all the handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex('^ℹ️ راهنما$'), help_command))
    dispatcher.add_handler(MessageHandler(Filters.regex('^🎧 دانلود از اسپاتیفای$'), handle_download_request))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'http://googleusercontent.com/spotify.com/4'), handle_playlist_link))

    updater.start_polling()
    logger.info("Bot is running...")
    updater.idle()


if __name__ == '__main__':
    main()
