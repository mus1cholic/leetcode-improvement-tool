from classes.Builders import Builder
from classes.Parsers import Parser
from bot.bot import Bot
from data import secret as secret

import discord

def main():
    # builder = Builder()
    # builder.build_question_rating_data()

    # parser = Parser()
    # parser.build_ratings()

    setup_bot()

def setup_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot(command_prefix="/", intents=intents)

    bot.run(secret.BOT_TOKEN)

if __name__ == "__main__":
    main()