from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message
from unidecode import unidecode

from os import getenv
from dotenv import load_dotenv
from random import choice

from readWords import readWordsJSON
from Enums import RedLetters, YellowLetters, BlueLetters
from Classes.game import Game, games
from utils import *

import server
from aiohttp import web

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")

PREFIX = ";"

words, dict_words_accents = readWordsJSON("../public/words.json")

bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print("Ready?")
    bot.server = server.HTTPServer(
        bot=bot,
        host="0.0.0.0",
        port="10000",
    )
    await bot.server.start()
    print("Go!")

@bot.command()
async def ping(ctx: Context):
    await ctx.channel.send(choice(words))

@bot.command(aliases=['s', "startGame", "ZEPARTIZEPARTI"])
async def start(ctx: Context, difficulty: str = "medium"):
    if doesGameExist(games, ctx.channel.id):
        await ctx.send("Il y a deja une partie en cours !")
        return
    
    random_word = getRandomWordByDifficulty(words, difficulty)

    game = Game(ctx.channel.id, random_word)

    game.setRandomCorrectLetters(2)

    await ctx.send("Démarrage de la partie. Mo Mo Motus !")
    await ctx.send(f"Entrez un mot de {len(random_word)} lettres")
    await ctx.send(game.correctLettersToString())
        
@bot.command()
async def test(ctx: Context, difficulty: str = "medium"):    
    random_word = getRandomWordByDifficulty(words, difficulty)
    await ctx.channel.send(dict_words_accents.get(random_word))
    await ctx.channel.send(findDefinitions(dict_words_accents.get(random_word)))

@bot.command()
async def stop(ctx: Context):
    if not doesGameExist(games, ctx.channel.id):
        await ctx.send("Il n'y a pas de partie en cours.")
        return
        
    game = games.get(ctx.channel.id)

    game.delete()

    await ctx.send("Partie terminée !")

@bot.event
async def on_message(message: Message):
    msg = unidecode(message.content).lower()

    # Pass message by bot
    if message.author == bot.user:
        return

    # Pass message not starting with prefix
    if msg.startswith(PREFIX):
        return await bot.process_commands(message)

    # Pass message if no active games in channel
    if not games.get(message.channel.id):
        return

    random_word = games.get(message.channel.id).word

    # Pass if the length of the word is not the same as the random_word
    if len(msg) != len(random_word):
        return

    if not msg in words:
        return await message.channel.send("Le mot que vous avez écrit n'est pas français.")


    game = games.get(message.channel.id)

    # Create a list with every valid letters
    list_letters = list(random_word)

    # [-, -, -, -, -, -]
    result = [BlueLetters.EMPTY for i in range(len(random_word))]

    # Set all correctly placed letters
    for i, letter in enumerate(msg):
        # If letter is correctly placed
        if letter == random_word[i]:
            # Remove letter from list
            index = list_letters.index(letter)
            list_letters.pop(index)

            # Replace - with valid letter

            letter_append = RedLetters[letter]

            game.correct[i] = letter_append
            result[i] = letter_append

        else:
            result[i] = BlueLetters[letter]

    # Set all letters not correctly placed
    for i, letter in enumerate(msg):
        # If letter is in the list of correct letters
        if letter in list_letters:
            # If letter is already placed continue
            if type(result[i]) != BlueLetters:
                continue

            # Remove letter from list
            index = list_letters.index(letter)
            list_letters.pop(index)

            # Replace - with incorrectly placed letter
            result[i] = YellowLetters[letter]
            
    historique = game.history
    historique.append(result)

    game.current += 1

    if len(historique) > 2:
        historique.pop(0)

    await message.channel.send(game.historyToString())

    if msg == game.word:
        game.delete()
        await message.channel.send(getRandomPhrase(message.author))
        await message.channel.send(findDefinitions(dict_words_accents.get(game.word)))
        return

    if game.current >= game.limit:
        await message.channel.send(f"Partie terminée ! Le mot était: {game.word}")
        game.delete()

@server.add_route(path="/", method="GET")
async def home(request):
    return web.json_response(data={"foo": "bar"}, status=200)  

@server.add_route(path="/healthcheck", method="GET")
async def home(request):
    return web.json_response(status=200)  

bot.run(DISCORD_TOKEN)
