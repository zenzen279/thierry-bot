# from pytrends.request import TrendReq
# from src.readWords import readWordsJSON

# pytrends = TrendReq(hl='fr', tz=360)


# def getResult(words):
#     kw_list = words # list of keywords to get data

#     a = pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo="FR")

#     data = pytrends.interest_over_time()
#     data = data.reset_index()
#     #print(data)
#     if data.empty:
#         return 0
#     return (data[kw_list].sum())

# words = readWordsJSON("../public/words.json")

# words = words[0:100]

# for i in range(len(words)):
#     words_cut = words[i:max(len(words), i+1)]
#     print(getResult(words_cut))

import requests
from bs4 import BeautifulSoup

word = "établons"


def scrapDefinition(url: str) -> list[str]:
    # Liste des bouts de phrases ou l'on doit refaire un scrapping pour trouver la bonne définition
    redos = ["pluriel de", "personne du", "participe passé"]

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Tout les li contenant des définitions
    definitions = soup.find("ol").find_all("li")

    definition = definitions[0]
    definition_text = definition.getText()

    # Si une string de la liste redos est dans la définition
    if any(redo for redo in redos if redo in definition_text.lower()):
        parent_url = "https://fr.wiktionary.org" + definition.find("a")["href"]
        return scrapDefinition(parent_url)

    # Liste de string avec tout les définition
    definitions_list = [definition.getText() for definition in definitions]

    return definitions_list[:5]


def findDefinitions(word: str):
    url = f"https://fr.wiktionary.org/w/index.php?search={word}"
    try:
        return scrapDefinition(url)
    except:
        return None


print(findDefinitions(word))
