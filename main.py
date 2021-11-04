from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message

from discord import Embed, Color

import unidecode

from os import getenv, read
from dotenv import load_dotenv

from readWords import readWords

from random import choice

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")

PREFIX = ";"

words = readWords().split('\n')

bot = commands.Bot(command_prefix=PREFIX)

curr_games = {}

@bot.event
async def on_ready():
    print("HELLO WORLDOU")


@bot.command()
async def ping(ctx: Context):
    await ctx.channel.send(choice(words))


@bot.command(aliases=['s', "startGame","ZEPARTIZEPARTI"])
async def start(ctx: Context):
    await ctx.send("Démarrage de la partie. Mo Mo Motus !")

    mot = choice(words)

    curr_games[ctx.guild.id] = {
        "mot": unidecode.unidecode(mot)
    }
    
    await ctx.send(f"Entrez un mot de {len(mot)} lettres")


# _ _ _ _ _ _ _
# J O U R N A L
# _ O u _ n _ _

@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    if message.content.startswith(PREFIX):
        return await bot.process_commands(message)

    if not message.guild.id in list(curr_games.keys()):
        return
        
    if len(message.content) != len(curr_games[message.guild.id]['mot']):
        return

    mot = message.content

    mot_mot = curr_games[message.guild.id]['mot']

    mot_mot2 = list(mot_mot)
    
    mot_to_send = []

    # RNAL
    # JOURANJN
    #ENFANT
    #6N66OT


    # lepiot
    # mouffle
    
    for i in range(len(mot)):    
        if mot[i].lower() == mot_mot[i].lower():
            index = mot_mot2.index(mot[i])
            mot_mot2.pop(index)

            mot_to_send.append(f" :regional_indicator_{mot[i].lower()}: ")
        else:
            mot_to_send.append(" - ")

    for i in range(len(mot)):   
        if any(mo for mo in mot_mot2 if mo.lower() == mot[i].lower()):
            if mot_to_send[i].startswith(" :regional_indicator_"):
                continue
            
            index = mot_mot2.index(mot[i])
            mot_mot2.pop(index)
            mot_to_send[i] = f" {mot[i].lower()} "

    await message.channel.send("".join(mot_to_send))

@bot.command()
async def triche(ctx:Context):
    await ctx.channel.send(curr_games[ctx.guild.id]['mot'])
# @bot.command()
# async def test(ctx: Context):
#     emoji = "<:g_letter:905855821735399455>"
#     await ctx.channel.send(emoji)

bot.run(DISCORD_TOKEN)