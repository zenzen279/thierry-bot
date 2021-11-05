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

    random_word = choice(words)

    curr_games[ctx.channel.id] = {
        "word": unidecode.unidecode(random_word).lower()
    }
    
    await ctx.send(f"Entrez un mot de {len(random_word)} lettres")


@bot.event
async def on_message(message: Message):
    # Pass message by bot
    if message.author == bot.user:
        return

    # Pass message not starting with prefix
    if message.content.startswith(PREFIX):
        return await bot.process_commands(message)

    # Pass message if no active games in channel
    if not message.channel.id in list(curr_games.keys()):
        return

    random_word = curr_games[message.channel.id]['word']

    # Pass if the length of the word is not the same as the random_word 
    if len(message.content) != len(random_word):
        return

    mot = message.content.lower()

    # Create a list with every valid letters
    list_letters = list(random_word)

    # [-, -, -, -, -, -]
    result = ["-" for i in range(len(random_word))]


    # Set all correctly placed letters
    for i, letter in enumerate(mot):  
        # If letter is correctly placed
        if letter == random_word[i]:
            # Remove letter from list
            index = list_letters.index(letter)
            list_letters.pop(index)

            # Replace - with valid letter 
            result[i] =  f":regional_indicator_{letter}:" 
    
    # Set all letters not correctly placed
    for i, letter in enumerate(mot):  
        # If letter is in the list of correct letters
        if letter in list_letters:
            # If letter is already placed continue
            if result[i].startswith(":regional_indicator_"):
                continue

            # Remove letter from list
            index = list_letters.index(letter)
            list_letters.pop(index)

            # Replace - with incorrectly placed letter
            result[i] = f"{letter}"

    await message.channel.send(" ".join(result))

@bot.command()
async def triche(ctx:Context):
    await ctx.channel.send(curr_games[ctx.channel.id]['word'])

# @bot.command()
# async def test(ctx: Context):
#     emoji = "<:g_letter:905855821735399455>"
#     await ctx.channel.send(emoji)

bot.run(DISCORD_TOKEN)