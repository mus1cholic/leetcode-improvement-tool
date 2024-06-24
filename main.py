from discord import Intents

from bot.bot import Bot
from classes.Builders import Builder
from classes.Parsers import Parser
from data.secret import BOT_TOKEN

def main():
    # builder = Builder()
    # builder.build_question_rating_data()

    # parser = Parser()
    # parser.build_ratings()

    setup_bot()

def setup_bot():
    intents = Intents.default()
    intents.message_content = True

    bot = Bot(command_prefix="/", intents=intents)

    bot.run(BOT_TOKEN)

if __name__ == "__main__":
    main()