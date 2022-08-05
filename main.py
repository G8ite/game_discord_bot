import discord
from discord.ext import commands
from Data.database_handler import DatabaseHandler
from gif_game_cog import Gif_game_cog 

bot = commands.Bot(command_prefix="/", description="bot de test")
database_handler = DatabaseHandler("Data/discord-bot.db")

@bot.event
async def on_ready():
    print("Ready")

bot.add_cog(Gif_game_cog(bot))

bot.run("MTAwNTA5OTM3MTYxMzkxMzEwOA.GxPQbS.EQjiHgdHqM9twrCPYZDptUSf05zLmcQmizowlY")