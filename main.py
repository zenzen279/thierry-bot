from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message

from discord import Embed, Color

import unidecode

from os import getenv
from dotenv import load_dotenv

from readWords import readWords

from random import choice

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")

PREFIX = ";"

words = readWords().split('\n')

bot = commands.Bot(command_prefix=PREFIX)

# TODO: Store the highest guess in Game class, (Score + 1 when a letter is good else score +.25)

class Game:
    def __init__(self, word):
        self.word = unidecode.unidecode(word).lower()

class Games:
    list = {}

    def __str__(self) -> str:
        return f"{len(self.list)} parties actives"

    def start(self, key: str, word: str) -> bool:
        if self.includes(key): 
            return False

        self.list[key] = Game(word)
        return True

    def stop(self, key: str) -> bool:
        try:
            del self.list[key]
            return True
        except:
            return False

    def get(self, key: str) -> Game:
        return self.list[key]

    def includes(self, key: str) -> bool:
        return key in list(self.list.keys())

games = Games()

@bot.event
async def on_ready():
    print("HELLO WORLDOU")


@bot.command()
async def ping(ctx: Context):
    await ctx.channel.send(choice(words))


@bot.command(aliases=['s', "startGame","ZEPARTIZEPARTI"])
async def start(ctx: Context):
    random_word = choice(words)

    res = games.start(ctx.channel.id, random_word)
    
    if res:
        await ctx.send("Démarrage de la partie. Mo Mo Motus !")
        await ctx.send(f"Entrez un mot de {len(random_word)} lettres")
    else:
        await ctx.send("Il y a deja une partie en cours !")

@bot.command()
async def stop(ctx: Context):
    if not games.includes(ctx.channel.id):
        return await ctx.send("Il n'y a pas de parties en cours")

    res = games.stop(ctx.channel.id)

    if res:
        await ctx.send("Partie terminée !")
    else:
        await ctx.send("Erreur durant l'arret de la partie.")
    
    

@bot.event
async def on_message(message: Message):
    # Pass message by bot
    if message.author == bot.user:
        return

    # Pass message not starting with prefix
    if message.content.startswith(PREFIX):
        return await bot.process_commands(message)

    # Pass message if no active games in channel
    if not games.includes(message.channel.id):
        return

    random_word = games.get(message.channel.id).word

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
    await ctx.channel.send(games.get(ctx.channel.id).word)

# @bot.command()
# async def test(ctx: Context):
#     emoji = "<:g_letter:905855821735399455>"
#     await ctx.channel.send(emoji)

bot.run(DISCORD_TOKEN)