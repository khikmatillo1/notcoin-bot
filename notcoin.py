import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

# Define the conversation states
BUY_SELL, CHOOSE_COIN, AMOUNT, PAYMENT_INFO = range(4)

# Define the live price of NotCoin and TonCoin (for demonstration purposes)
NOTCOIN_PRICE = 0.5  # $0.5 per NotCoin
TONCOIN_PRICE = 1.0  # $1.0 per TonCoin

# Define the buy/sell keyboard
buy_sell_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("Buy", callback_data="buy"),
    InlineKeyboardButton("Sell", callback_data="sell")
]])

# Define the coin choice keyboard
coin_choice_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("NotCoin", callback_data="notcoin"),
    InlineKeyboardButton("TonCoin", callback_data="toncoin")
]])

# Define the payment info keyboard
payment_info_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("Pay with Card", callback_data="pay_card")
]])

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose an option:", reply_markup=buy_sell_keyboard)
    return BUY_SELL

def buy_sell_choice(update, context):
    query = update.callback_query
    choice = query.data

    if choice == "buy":
        query.edit_message_text(text="Select the coin you want to buy:")
        query.edit_message_reply_markup(reply_markup=coin_choice_keyboard)
        return CHOOSE_COIN
    elif choice == "sell":
        query.edit_message_text(text="Select the coin you want to sell:")
        query.edit_message_reply_markup(reply_markup=coin_choice_keyboard)
        return CHOOSE_COIN

def choose_coin(update, context):
    query = update.callback_query
    coin = query.data

    if coin == "notcoin":
        query.edit_message_text(text="Enter the amount of NotCoin you want to buy/sell:")
        context.user_data["coin"] = "notcoin"
        return AMOUNT
    elif coin == "toncoin":
        query.edit_message_text(text="Enter the amount of TonCoin you want to buy/sell:")
        context.user_data["coin"] = "toncoin"
        return AMOUNT

def amount(update, context):
    query = update.callback_query
    amount = query.data

    if context.user_data["coin"] == "notcoin":
        total_amount = int(amount) * NOTCOIN_PRICE
    else:
        total_amount = int(amount) * TONCOIN_PRICE

    query.edit_message_text(text=f"You want to buy/sell {amount} {context.user_data['coin']}.\nTotal amount: ${total_amount:.2f}")
    query.edit_message_reply_markup(reply_markup=payment_info_keyboard)
    return PAYMENT_INFO

def payment_info(update, context):
    query = update.callback_query
    query.edit_message_text(text="Please enter your payment information:")

    context.bot.send_message(chat_id=update.effective_chat.id, text="Name:")
    context.user_data["state"] = "name"
    return PAYMENT_INFO

def get_payment_info(update, context):
    user_input = update.message.text

    if context.user_data["state"] == "name":
        context.user_data["name"] = user_input
        context.bot.send_message(chat_id=update.effective_chat.id, text="Last Name:")
        context.user_data["state"] = "last_name"
    elif context.user_data["state"] == "last_name":
        context.user_data["last_name"] = user_input
        context.bot.send_message(chat_id=update.effective_chat.id, text="Wallet Address:")
        context.user_data["state"] = "wallet_address"
    elif context.user_data["state"] == "wallet_address":
        context.user_data["wallet_address"] = user_input
        context.bot.send_message(chat_id=update.effective_chat.id, text="Payment information received. Thank you!")
        return ConversationHandler.END

def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Operation canceled.")
    return ConversationHandler.END

def main():
    updater = Updater("7370183618:AAHwTafN1cXrCR-FOv9T6zcWNSdu4NUFjh0", use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            BUY_SELL: [CallbackQueryHandler(buy_sell_choice)],
            CHOOSE_COIN: [CallbackQueryHandler(choose_coin)],
            AMOUNT: [CallbackQueryHandler(amount)],
            PAYMENT_INFO: [CallbackQueryHandler(payment_info), MessageHandler(filters.Text & ~filters.Command, get_payment_info)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

# if __name__ == "__main__":
#     main()
