import os
from discord.ext import commands
from gif_game_cog import Gif_game_cog
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="/", description="bot de test")
load_dotenv(dotenv_path="config")

@bot.event
async def on_ready():
    print("Ready")

bot.add_cog(Gif_game_cog(bot))

bot.run(os.getenv("TOKEN"))