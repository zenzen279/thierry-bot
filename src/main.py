from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message
from unidecode import unidecode

from os import getenv
from dotenv import load_dotenv
from random import choice

from readWords import readWordsJSON
from Enums import RedLetters, YellowLetters, BlueLetters, FilteredWordsLambdas


load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")
PREFIX = ";"

words = readWordsJSON("../public/words.json")

bot = commands.Bot(command_prefix=PREFIX)

games = {}

class Game:
    def __init__(self, id,  word, limit: int = 10):
        self.id = id
        self.word = word
        self.limit = limit
        self.current = 0
        self.history = []
        self.correct = [BlueLetters.EMPTY for i in range(len(self.word))]
        
        games[id] = self
    
    def delete(self):
        del games[self.id]

    def setRandomCorrectLetters(self, n: int):
        for i in range(n):
            letter = choice(self.word)
            index = self.word.index(letter)
            self.correct[index] = RedLetters[letter]
        
    def correctLettersToString(self):
        return " ".join(self.correct)

@bot.event
async def on_ready():
    print("HELLO WORLDOU")


@bot.command()
async def ping(ctx: Context):
    await ctx.channel.send(choice(words))

def doesGameExist(id):
    curr_game = games.get(id, None)

    if curr_game is None:
        return False
        
    return True

def getRandomWordByDifficulty(difficulty: str):
    filtered_words = list(filter(FilteredWordsLambdas[difficulty], words))

    random_word = choice(filtered_words)  

    return random_word

@bot.command(aliases=['s', "startGame", "ZEPARTIZEPARTI"])
async def start(ctx: Context, difficulty: str = "medium"):
    if not doesGameExist(ctx.channel.id):
        await ctx.send("Il y a deja une partie en cours !")
    
    random_word = getRandomWordByDifficulty(difficulty)

    game = Game(ctx.channel.id, random_word)

    game.setRandomCorrectLetters(2)

    await ctx.send("Démarrage de la partie. Mo Mo Motus !")
    await ctx.send(f"Entrez un mot de {len(random_word)} lettres")
    await ctx.send(game.correctLettersToString())
        
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
    msg = unidecode(message.content).lower()

    # Pass message by bot
    if message.author == bot.user:
        return

    # Pass message not starting with prefix
    if msg.startswith(PREFIX):
        return await bot.process_commands(message)

    # Pass message if no active games in channel
    if not games.includes(message.channel.id):
        return

    random_word = games.get(message.channel.id).word

    # Pass if the length of the word is not the same as the random_word
    if len(msg) != len(random_word):
        return

    if not msg in words:
        return await message.channel.send("Le mot que vous avez écrit n'est pas français.")


    current_game = games.get(message.channel.id)

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

            current_game.correct[i] = letter_append
            result[i] = letter_append

        else:
            result[i] = BlueLetters[letter]

    # Set all letters not correctly placed
    for i, letter in enumerate(msg):
        # If letter is in the list of correct letters
        if letter in list_letters:
            # If letter is already placed continue
            if result[i].startswith("<:"):
                continue

            # Remove letter from list
            index = list_letters.index(letter)
            list_letters.pop(index)

            # Replace - with incorrectly placed letter
            result[i] = YellowLetters[letter]

    result_str = " ".join(result)

    historique = current_game.history
    historique.append(result_str)

    current_game.current += 1

    if len(historique) > 2:
        historique.pop(0)

    await message.channel.send("\n".join(historique) + "\n" + " ".join(current_game.correct))

    if msg == current_game.word:
        games.stop(message.channel.id)
        return await message.channel.send("Bravo !!! Vous avez gagné !!!")

    if current_game.current >= current_game.limit:
        await message.channel.send(f"Partie términée ! Le mot etait: {current_game.word}")
        games.stop(message.channel.id)

bot.run(DISCORD_TOKEN)
