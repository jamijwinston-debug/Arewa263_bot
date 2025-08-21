import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration with your specific details
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7317949191:AAGupvYPiLzNSq3TbYG1UljcOZ2XohibHSs')
CHANNEL_USERNAME = os.environ.get('CHANNEL_USERNAME', 'Yakstaschannel')
GROUP_USERNAME = os.environ.get('GROUP_USERNAME', 'yakstascapital')
TWITTER_USERNAME = os.environ.get('TWITTER_USERNAME', 'bigbangdist10')

# Store user progress
user_data = {}

# Start command
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data[user_id] = {'state': 'join_channel'}
    
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton("I've Joined", callback_data="joined_channel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "Welcome to Mr. Kayblezzy2 Airdrop! 🚀\n\n"
        "To qualify for the airdrop, complete these tasks:\n\n"
        "1. Join our channel\n"
        "2. Join our group\n"
        "3. Follow our Twitter\n"
        "4. Submit your Solana wallet address\n\n"
        "Start by joining our channel:",
        reply_markup=reply_markup
    )

# Handle channel join callback
def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    
    if query.data == "joined_channel":
        user_data[user_id]['state'] = 'join_group'
        keyboard = [
            [InlineKeyboardButton("Join Group", url=f"https://t.me/{GROUP_USERNAME}")],
            [InlineKeyboardButton("I've Joined", callback_data="joined_group")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            "Great! Now join our group:",
            reply_markup=reply_markup
        )
    
    elif query.data == "joined_group":
        user_data[user_id]['state'] = 'follow_twitter'
        keyboard = [
            [InlineKeyboardButton("Follow Twitter", url=f"https://twitter.com/{TWITTER_USERNAME}")],
            [InlineKeyboardButton("I'm Following", callback_data="followed_twitter")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            "Awesome! Now follow our Twitter:",
            reply_markup=reply_markup
        )
    
    elif query.data == "followed_twitter":
        user_data[user_id]['state'] = 'submit_wallet'
        query.edit_message_text(
            "Perfect! Now send me your Solana wallet address to complete the qualification."
        )

# Handle wallet submission
def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_state = user_data.get(user_id, {}).get('state')
    
    if user_state == 'submit_wallet':
        # Simple validation for Solana wallet (basic format check)
        wallet_address = update.message.text.strip()
        
        # Basic Solana address validation (32-44 characters)
        if len(wallet_address) >= 32 and len(wallet_address) <= 44:
            user_data[user_id]['state'] = 'completed'
            user_data[user_id]['wallet'] = wallet_address
            
            update.message.reply_text(
                "🎉 Congratulations! You've qualified for Mr. Kayblezzy2's airdrop!\n\n"
                "Well done, hope you didn't cheat the system. 😉\n"
                "10 SOL is on its way to your address!\n\n"
                "Thank you for participating!"
            )
        else:
            update.message.reply_text(
                "That doesn't look like a valid Solana wallet address. "
                "Please check and submit again."
            )

# Error handler
def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Main function
def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(BOT_TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Log all errors
    dp.add_error_handler(error)
    
    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
