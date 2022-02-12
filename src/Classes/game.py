from Enums import RedLetters, YellowLetters, BlueLetters
from random import choice
from utils import enumsToString

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
        return enumsToString(self.correct)

    def historyToString(self):
        enums = "\n".join(map(enumsToString,self.history))
        correct_letters = "\n" + self.correctLettersToString()
        return enums + correct_letters