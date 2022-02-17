import json
import os
from pathlib import Path
from unidecode import unidecode

def readWordsJSON(path: str):
    dir_name = os.path.dirname(__file__)

    path = str(Path(dir_name, path).resolve())
    
    with open(path, "r", encoding="utf-8") as file:
        words = json.load(file)
        return [unidecode(word.lower()) for word in words], {unidecode(word.lower()): word.lower() for word in words}