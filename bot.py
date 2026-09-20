import telebot
from config import BOT_TOKEN
from database import Database
from handlers import BotHandlers


def main():
    bot = telebot.TeleBot(BOT_TOKEN)
    Database.create_tables()
    handlers = BotHandlers(bot)
    handlers.register_handlers()
    bot.infinity_polling()


if __name__ == "__main__":
    main()
