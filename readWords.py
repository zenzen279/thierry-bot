def readWords(path: str = "./words.txt"):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except:
        return ""

import json

def readWordsJSON(path: str = "./mots.json"):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return ""