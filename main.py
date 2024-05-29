from classes.Builders import Builder
from classes.Parsers import Parser
from bot.bot import Bot
from data import secret as secret

from utils.extrapolate import build_regression_fit

import discord

def main():
    # TODO: eventually do npm run dev on another thread here
    builder = Builder()

    #builder.build_question_rating_data()

    build_regression_fit()

    # setup_bot()

def setup_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot(command_prefix="/", intents=intents)

    bot.run(secret.BOT_TOKEN)

if __name__ == "__main__":
    main()