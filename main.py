from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message

from discord import Embed, Color

import unidecode

from os import getenv
from dotenv import load_dotenv

from readWords import readWordsJSON

from random import choice

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")

PREFIX = ";"


french_words = [unidecode.unidecode(word).lower() for word in readWordsJSON("./words.json")]

print(len(french_words))

words = readWordsJSON()

bot = commands.Bot(command_prefix=PREFIX)

# TODO: Store the highest guess in Game class, (Score + 1 when a letter is good else score +.25)


class Game:
    def __init__(self, word, limit: int = 10):
        self.word = unidecode.unidecode(word).lower()
        self.limit = limit
        self.current = 0
        self.history = []
        self.correct = [
            "<:BLEU:906229080985317398>" for i in range(len(self.word))]


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


def getRedLetter(letter: str) -> str:
    match letter:
        case "a":
            return "<:A:906222600789819492>"
        case "b":
            return "<:B:906224175444807730>"
        case "c":
            return "<:C:906224175381880832>"
        case "d":
            return "<:D:906224175365103696>"
        case "e":
            return "<:E:906224175574839316>"
        case "f":
            return "<:F:906224175331557397>"
        case "g":
            return "<:G:906224175100878859>"
        case "h":
            return "<:H:906224175407038464>"
        case "i":
            return "<:I:906224175658713160>"
        case "j":
            return "<:J:906224175423815690>"
        case "k":
            return "<:K:906224175440609301>"
        case "l":
            return "<:L:906224175474171914>"
        case "m":
            return "<:M:906224175474176020>"
        case "n":
            return "<:N:906224175511920640>"
        case "o":
            return "<:O:906224175352537099>"
        case "p":
            return "<:P:906224175344132117>"
        case "q":
            return "<:Q:906224175499325510>"
        case "r":
            return "<:R:906224175570632704>"
        case "s":
            return "<:S:906224175201538070>"
        case "t":
            return "<:T:906224175310581781>"
        case "u":
            return "<:U:906224175700664350>"
        case "v":
            return "<:V:906224175683874845>"
        case "w":
            return "<:W:906224175625175090>"
        case "x":
            return "<:X:906224175293825046>"
        case "y":
            return "<:Y:906224175583215626>"
        case "z":
            return "<:Z:906224175650332682>"


def getYellowLetter(letter: str) -> str:
    match letter:
        case "a":
            return "<:Aj:906226090643689532>"
        case "b":
            return "<:Bj:906226090882760734>"
        case "c":
            return "<:Cj:906226093453881344>"
        case "d":
            return "<:Dj:906226093630050315>"
        case "e":
            return "<:Ej:906226093198028874>"
        case "f":
            return "<:Fj:906226093688778792>"
        case "g":
            return "<:Gj:906226093634252851>"
        case "h":
            return "<:Hj:906226093617463307>"
        case "i":
            return "<:Ij:906226091386085386>"
        case "j":
            return "<:Jj:906226093864931388>"
        case "k":
            return "<:Kj:906226093676199976>"
        case "l":
            return "<:Lj:906226093663588384>"
        case "m":
            return "<:Mj:906226093726502922>"
        case "n":
            return "<:Nj:906226093525196821>"
        case "o":
            return "<:Oj:906226093856530462>"
        case "p":
            return "<:Pj:906226093940432936>"
        case "q":
            return "<:Qj:906226093986566174>"
        case "r":
            return "<:Rj:906226094011723806>"
        case "s":
            return "<:Sj:906226094158528533>"
        case "t":
            return "<:Tj:906226094103986206>"
        case "u":
            return "<:Uj:906226094343073792>"
        case "v":
            return "<:Vj:906226094120788068>"
        case "w":
            return "<:Wj:906227753093845073>"
        case "x":
            return "<:Xj:906227753777512458>"
        case "y":
            return "<:Yj:906227753618116628>"
        case "z":
            return "<:Zj:906227753446162482>"


@bot.event
async def on_ready():
    print("HELLO WORLDOU")


@bot.command()
async def ping(ctx: Context):
    await ctx.channel.send(choice(words))


@bot.command(aliases=['s', "startGame", "ZEPARTIZEPARTI"])
async def start(ctx: Context, difficulty: str = "medium"):
    words_list = words

    match difficulty.lower():
        case "easy":
            words_list = list(filter(lambda x: len(x) < 6, words_list))
        case "medium":
            words_list = list(filter(lambda x: 5 < len(x) < 9, words_list))
        case "hard":
            words_list = list(filter(lambda x: 8 < len(x), words_list))

    random_word = choice(words_list)

    res = games.start(ctx.channel.id, random_word)

    if res:
        curr_game = games.get(ctx.channel.id)

        for i in range(2):
            letter = choice(curr_game.word)
            index = curr_game.word.index(letter)
            curr_game.correct[index] = getRedLetter(letter)

        await ctx.send("Démarrage de la partie. Mo Mo Motus !")
        await ctx.send(f"Entrez un mot de {len(random_word)} lettres")
        await ctx.send(" ".join(curr_game.correct))
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
    msg = unidecode.unidecode(message.content).lower()

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

    if not msg in french_words:
        return await message.channel.send("Le mot que vous avez écrit n'est pas français.")


    current_game = games.get(message.channel.id)

    # Create a list with every valid letters
    list_letters = list(random_word)

    # [-, -, -, -, -, -]
    result = ["<:BLEU:906229080985317398>" for i in range(len(random_word))]

    # Set all correctly placed letters
    for i, letter in enumerate(msg):
        # If letter is correctly placed
        if letter == random_word[i]:
            # Remove letter from list
            index = list_letters.index(letter)
            list_letters.pop(index)

            # Replace - with valid letter
            letter_append = getRedLetter(letter)

            current_game.correct[i] = letter_append
            result[i] = letter_append

        else:
            result[i] = f":regional_indicator_{letter}:"

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
            result[i] = getYellowLetter(letter)

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
