import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fake balance for demonstration
fake_balance = 1000

# Define a few command handlers
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    keyboard = [
        [InlineKeyboardButton("Buy Notcoin", callback_data='buy_notcoin')],
        [InlineKeyboardButton("Check Balance", callback_data='check_balance')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome to Notcoin Bot! Choose an option:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Handle button clicks."""
    query = update.callback_query
    query.answer()

    if query.data == 'buy_notcoin':
        # Here you would integrate with a payment processor or blockchain
        global fake_balance
        if fake_balance > 0:
            fake_balance -= 1  # Decrement balance for the demo
            query.edit_message_text(text=f"Thank you for buying Notcoin! Your remaining balance is {fake_balance} Notcoins.")
        else:
            query.edit_message_text(text="Sorry, you have no Notcoins left to buy.")
    elif query.data == 'check_balance':
        query.edit_message_text(text=f"Your current balance is {fake_balance} Notcoins.")

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Use /start to interact with the bot.')

def main() -> None:
    """Start the bot."""
    # Insert your API token here
    TOKEN = 'YOUR_API_TOKEN_HERE'

    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # On different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
