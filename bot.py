from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7317949191:AAGupvYPiLzNSq3TbYG1UljcOZ2XohibHSs')
CHANNEL_USERNAME = os.environ.get('CHANNEL_USERNAME', '@Yakstaschannel')
GROUP_USERNAME = os.environ.get('GROUP_USERNAME', '@yakstascapital')
TWITTER_USERNAME = os.environ.get('TWITTER_USERNAME', '@bigbangdist10')

# Store user progress (in production, use a database)
user_data = {}

# Define conversation states
(
    START,
    JOIN_CHANNEL,
    JOIN_GROUP,
    FOLLOW_TWITTER,
    SUBMIT_WALLET,
    COMPLETED
) = range(6)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {'state': JOIN_CHANNEL}
    
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("I've Joined", callback_data="joined_channel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
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
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "joined_channel":
        user_data[user_id]['state'] = JOIN_GROUP
        keyboard = [
            [InlineKeyboardButton("Join Group", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
            [InlineKeyboardButton("I've Joined", callback_data="joined_group")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Great! Now join our group:",
            reply_markup=reply_markup
        )
    
    elif query.data == "joined_group":
        user_data[user_id]['state'] = FOLLOW_TWITTER
        keyboard = [
            [InlineKeyboardButton("Follow Twitter", url=f"https://twitter.com/{TWITTER_USERNAME[1:]}")],
            [InlineKeyboardButton("I'm Following", callback_data="followed_twitter")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Awesome! Now follow our Twitter:",
            reply_markup=reply_markup
        )
    
    elif query.data == "followed_twitter":
        user_data[user_id]['state'] = SUBMIT_WALLET
        await query.edit_message_text(
            "Perfect! Now send me your Solana wallet address to complete the qualification."
        )

# Handle wallet submission
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state = user_data.get(user_id, {}).get('state')
    
    if user_state == SUBMIT_WALLET:
        # Simple validation for Solana wallet (basic format check)
        wallet_address = update.message.text.strip()
        
        if len(wallet_address) >= 32 and len(wallet_address) <= 44:
            user_data[user_id]['state'] = COMPLETED
            user_data[user_id]['wallet'] = wallet_address
            
            await update.message.reply_text(
                "🎉 Congratulations! You've qualified for Mr. Kayblezzy2's airdrop!\n\n"
                "Well done, hope you didn't cheat the system. 😉\n"
                "10 SOL is on its way to your address!\n\n"
                "Thank you for participating!"
            )
        else:
            await update.message.reply_text(
                "That doesn't look like a valid Solana wallet address. "
                "Please check and submit again."
            )

# Set up Telegram application
def setup_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    return application

# Flask routes
@app.route('/')
def home():
    return "Mr. Kayblezzy2 Airdrop Bot is running!"

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # In production, you would set up a webhook here
    return "Webhook would be set up in production environment"

# Run the application
if __name__ == '__main__':
    # For development
    bot_application = setup_bot()
    
    # Start the bot in polling mode (for development)
    # In production, you would use webhooks instead
    print("Starting bot in polling mode...")
    bot_application.run_polling()
