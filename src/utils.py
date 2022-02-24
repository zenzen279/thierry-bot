import requests

from random import choice
from bs4 import BeautifulSoup

def doesGameExist(games, id):
    curr_game = games.get(id, None)

    if curr_game is None:
        return False
        
    return True

def enumsToString(enum_list):
    return " ".join(map(lambda l: l.value,enum_list))

def getRandomWordByDifficulty(words, difficulty: str):
    filter_enum = difficulty_filters[difficulty]

    filtered_words = list(filter(filter_enum, words))

    random_word = choice(filtered_words)  

    return random_word
    
def getRandomPhrase(user):
    if user.id == 346417942575185922:
        return "Wow bravo Mélanie tu es vraiment très forte, ça me fait très plaisir que tu joues à mon jeu."

    phrases = [
        f"Bravo {user.name}, tu as trouvé le mot.",
        f"C'est presque trop facile pour toi {user.name}, bravo.",
        f"Tu as trouvé le mot, mais tu as eu de la chance {user.name}.",
        f"{user.name} a trouvé la réponse ! Mo Mo Motus !",
        f"Bravo {user.name}, tu es un champion !"
    ]
    
    return choice(phrases)

def scrapDefinition(url: str) -> list[str]:
    # Liste des bouts de phrases ou l'on doit refaire un scrapping pour trouver la bonne définition
    redos = ["pluriel de", "personne du", "du verbe"]

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Tout les li contenant des définitions
    definitions = soup.find("ol").find_all("li")

    definition = definitions[0]
    definition_text = definition.getText()

    # Si une string de la liste redos est dans la définition
    if any(redo for redo in redos if redo in definition_text.lower()):
        parent_url = "https://fr.wiktionary.org" + definition.find("a")["href"]
        return scrapDefinition(parent_url)

    return definition_text
        
def findDefinitions(word: str): 
    url = f"https://fr.wiktionary.org/w/index.php?search={word}"
    try:
        return scrapDefinition(url)
    except:
        return "Franchement même le bot a pas trouvé la définition donc c'est pas grave si t'as pas trouvé."

difficulty_filters = {
    "easy": lambda x: (len(x) < 6),
    "medium": lambda x: (5 < len(x) < 9),
    "hard": lambda x: (8 < len(x))
}