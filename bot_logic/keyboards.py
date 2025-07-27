from telegram import ReplyKeyboardMarkup, KeyboardButton

# Define the layout of the main menu
main_menu_keyboard = ReplyKeyboardMarkup(
    [
        # First row
        [KeyboardButton("🎧 دانلود از اسپاتیفای")],
        # Second row
        [KeyboardButton("ℹ️ راهنما")]
    ],
    # Makes the keyboard fit the screen better
    resize_keyboard=True
)
