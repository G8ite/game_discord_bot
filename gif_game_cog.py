import asyncio
import json
import random

import requests
from discord.ext import commands

from Data.database_handler import DatabaseHandler


class Gif_game_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.database_handler = DatabaseHandler("Data/discord-bot.db")
        self.players = []


    
    @commands.command(name="gifgame", help="Lance un concours de gif")
    async def gifgame(self, ctx):
        await ctx.send("Attention, le concours de GIF va bientôt commencer,\n Pour participer, écrivez \"moi\" dans ce channel")
        def checkMessages(message):
            """Vérifie si le message écrit est bien dans le channel concerné par le jeu, si le joueur n'est pas déjà inscrit
                et si le message est bien 'moi'

            Args:
                message (str): message envoyé par un utilisateur

            Returns:
                bool: True ou False
            """
            return message.channel == ctx.message.channel and message.author.display_name not in self.players and message.content == "moi"
        async def add_user_db(user_name):
            """Ajoute un utilisateur à la base de données s'il n'y est pas encore

            Args:
                user_name (str): pseudo de l'utilisateur
            """
            result = self.database_handler.add_user(user_name)
            if result == 0 :
                print("Déjà dans le db")
            else:
                await ctx.send(f"Bienvenue dans la base de données {user_name} !")

        async def generate_meme(ctx):
            """Fait appel à l'api imgflip, affiche un meme et envoie aux joueurs le lien pour pouvoir le créer

            Args:
                ctx (discord.Context): serveur et channel concerné
            """
            url = "https://api.imgflip.com/get_memes"

            response = requests.request("GET", url)

            json_response = response.json()

            nbr = random.randint(0, len(json_response['data']['memes']))

            memes = json_response['data']['memes']
            img_meme = memes[nbr]['url']
            url_name = memes[nbr]['name']
            url_name_replace = url_name.replace(' ','-')
            url_name_replace = url_name_replace.replace("'","")
            url_begin = "https://imgflip.com/memegenerator/"
            await ctx.send(f"A vous de jouer : \n{img_meme}\n{url_begin}{url_name_replace}") 

        try:
            while True:
                participation = await self.bot.wait_for('message', timeout = 10, check=checkMessages)
                self.players.append(participation.author.display_name)
                add_user_db(participation.author.display_name)
                await ctx.send(f"{participation.author.display_name} participe au concours, il commencera dans 10 sec")
        except asyncio.TimeoutError:
            if len(self.players) == 0:
                await ctx.send("Personne ne s'est inscrit !")
            else:
                print("Début")
                generate_meme(ctx)
                self.active = True
                await ctx.send(f"Le concours commence, vous aurez 15 minutes pour proposer votre meilleur meme")
