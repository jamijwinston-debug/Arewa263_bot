import os
import random
import logging
from dotenv import load_dotenv

from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ChatType  # Use enum for chat types

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Predefined welcome messages
WELCOME_MESSAGES = [
    "🎉 Welcome {name} to the group! We're excited to have you here!",
    "👋 Hello {name}! Great to see you joining our community!",
    "🌟 Welcome aboard, {name}! Feel free to introduce yourself!",
    "😊 Hey {name}! We're thrilled to have you with us!",
    "🌈 Welcome {name}! You've just made this group even better!",
    "🚀 Hello {name}! Ready for an amazing time in our group?",
    "🎊 Welcome {name}! Don't be shy, say hello to everyone!",
    "🤗 Hi {name}! We've been waiting for someone like you!",
    "🌻 Welcome {name}! Make yourself at home!",
    "🔥 {name} has joined the party! Welcome!",
    "💫 Hello {name}! Your presence makes this group shine brighter!",
    "🎈 Welcome {name}! Let the fun begin!",
    "👑 Welcome {name}! You've just upgraded our group!",
    "🌠 Hey {name}! Great things happen when great people gather!",
    "🍕 Welcome {name}! You're just in time for the fun!",
]

# Predefined bot detection messages
BOT_WELCOME_MESSAGES = [
    "🤖 Looks like we have a new bot in town! Welcome {name}!",
    "⚡ A new bot has joined! Welcome {name} to our digital family!",
    "🔧 Technical alert! Bot {name} has joined the group!",
    "💻 Welcome our new robotic member, {name}!",
    "🤖 {name} has joined! Beep boop - welcome bot!",
    "⚙️ Automated welcome for our new bot friend, {name}!",
    "🔌 Powering up welcome for bot {name}!",
    "📟 Hello {name}! Your binary presence is noted!",
    "🤖 Welcome {name}! Ready to automate some fun?",
    "💾 New bot detected: {name}. Welcome to the system!",
]

# Over 100 predefined responses for normal interactions
PREDEFINED_RESPONSES = [
    "That's interesting! 🤔",
    "I never thought about it that way! 💡",
    "Great point! 👍",
    "I agree with you! ✅",
    "That's hilarious! 😂",
    "Wow, that's amazing! 🌟",
    "I'm learning so much from this group! 📚",
    "That's a good question! ❓",
    "Let me think about that... 🤔",
    "I'm here to help! 💪",
    "That's so true! ✅",
    "I appreciate your perspective! 🙏",
    "That's food for thought! 🍎",
    "Interesting take! 🎯",
    "I'm listening... 👂",
    "That's worth discussing! 💬",
    "I like your style! 😎",
    "That's insightful! 🔍",
    "Good to know! ℹ️",
    "I'm impressed! 👏",
    "That's helpful information! 💡",
    "I see what you mean! 👀",
    "That's a valid point! ✅",
    "I'm enjoying this conversation! 😊",
    "That's creative thinking! 🎨",
    "I appreciate that! 🙌",
    "That's well said! 🗣️",
    "I'm here for this! 🎯",
    "That's a great observation! 👁️",
    "I'm taking notes! 📝",
    "That's impressive! 🏆",
    "I like where this is going! 🚀",
    "That's thoughtful! 💭",
    "I'm learning something new! 🎓",
    "That's a good reminder! ⏰",
    "I value your input! 💎",
    "That's a cool idea! ❄️",
    "I'm glad you shared that! 🤗",
    "That's a powerful statement! 💪",
    "I'm curious to know more! 🔍",
    "That's a beautiful thought! 🌸",
    "I'm here to support! 🤝",
    "That's a smart approach! 🧠",
    "I'm excited about this! 🎉",
    "That's a kind thing to say! ❤️",
    "I'm always learning! 📖",
    "That's a positive outlook! ☀️",
    "I'm grateful for this chat! 🙏",
    "That's a wonderful idea! 🌈",
    "I'm paying attention! 👀",
    "That's a great suggestion! 💡",
    "I'm here to chat! 💬",
    "That's an important point! ⚠️",
    "I'm enjoying the discussion! 🎭",
    "That's a fresh perspective! 🌱",
    "I'm here to make friends! 👥",
    "That's a valuable insight! 💰",
    "I'm all ears! 👂",
    "That's a brilliant thought! 💎",
    "I'm here to spread positivity! 🌞",
    "That's a constructive comment! 🏗️",
    "I'm here to learn! 🎓",
    "That's a meaningful contribution! 🌟",
    "I'm here to engage! 🔄",
    "That's a thoughtful response! 💭",
    "I'm here to connect! 🔗",
    "That's a helpful comment! 🤝",
    "I'm here to share! 📤",
    "That's an interesting angle! 📐",
    "I'm here to participate! 🎯",
    "That's a wise observation! 🦉",
    "I'm here to contribute! 🎁",
    "That's a genuine comment! 💎",
    "I'm here to interact! 🤝",
    "That's a positive vibe! 🌈",
    "I'm here to communicate! 📞",
    "That's a great analogy! ⚖️",
    "I'm here to exchange ideas! 🔄",
    "That's a profound thought! 🌊",
    "I'm here to build community! 🏘️",
    "That's a useful tip! 💡",
    "I'm here to make a difference! 🌟",
    "That's a cool perspective! ❄️",
    "I'm here to add value! 💎",
    "That's a nice way to put it! 👍",
    "I'm here to be part of the conversation! 💬",
    "That's a valid opinion! ✅",
    "I'm here to share knowledge! 📚",
    "That's an awesome comment! 🤩",
    "I'm here to support everyone! 🤗",
    "That's a great point of view! 👁️",
    "I'm here to make everyone smile! 😊",
    "That's a wonderful thought! 🌟",
    "I'm here to create connections! 🔗",
    "That's a smart observation! 🧠",
    "I'm here to spread joy! 🎉",
    "That's a beautiful sentiment! ❤️",
    "I'm here to be helpful! 💪",
    "That's an excellent point! 🏅",
    "I'm here to make new friends! 👋",
]

RESPONSE_PROBABILITY = 0.30  # tweak as you like

class WelcomeBot:
    def __init__(self, token: str):
        self.application = (
            Application.builder()
            .token(token)
            .post_init(self.post_init)  # attach post_init the recommended way
            .build()
        )
        self.setup_handlers()

    def setup_handlers(self) -> None:
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))

        # Status updates: new members
        self.application.add_handler(
            MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, self.welcome_new_members)
        )

        # Group text messages (non-commands)
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        # Error handler
        self.application.add_error_handler(self.error_handler)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Hello! I'm a welcome bot. I'll greet new members and chat with everyone in the group! 🎉"
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        help_text = (
            "🤖 Welcome Bot Help:\n\n"
            "I automatically welcome new members when they join the group!\n"
            "I can also chat with everyone using my predefined responses.\n\n"
            "Commands:\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n\n"
            "Features:\n"
            "✅ Welcome new members\n"
            "✅ Detect and announce bots\n"
            "✅ Chat with group members\n"
            "✅ Send messages without being mentioned"
        )
        await update.message.reply_text(help_text)

    async def welcome_new_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        for new_member in update.message.new_chat_members:
            if new_member.id == context.bot.id:
                await update.message.reply_text(
                    "Thanks for adding me! I'll help welcome new members to this group! 🎉"
                )
                continue

            # Build display name
            user_name = new_member.first_name or ""
            if new_member.last_name:
                user_name += f" {new_member.last_name}"

            if new_member.is_bot:
                welcome_message = random.choice(BOT_WELCOME_MESSAGES).format(name=user_name)
            else:
                welcome_message = random.choice(WELCOME_MESSAGES).format(name=user_name)

            await update.message.reply_text(welcome_message)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Only respond in groups/supergroups
        if update.message and update.message.chat and update.message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            if random.random() < RESPONSE_PROBABILITY:
                await update.message.reply_text(random.choice(PREDEFINED_RESPONSES))

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.error("Update caused error", exc_info=context.error)

    async def post_init(self, application: Application) -> None:
        await application.bot.set_my_commands(
            [
                BotCommand("start", "Start the bot"),
                BotCommand("help", "Show help message"),
            ]
        )

    def run(self) -> None:
        # drop_pending_updates=True avoids replaying old updates after downtime
        self.application.run_polling(drop_pending_updates=True)

def main() -> None:
    if not BOT_TOKEN:
        raise ValueError("Please set BOT_TOKEN environment variable")
    print("Bot is running...")
    WelcomeBot(BOT_TOKEN).run()

if __name__ == "__main__":
    main()
