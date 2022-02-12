from enum import Enum

class FilteredWordsLambdas(Enum):
    EASY = lambda x: len(x) < 6
    MEDIUM = lambda x: 5 < len(x) < 9
    HARD = lambda x: 8 < len(x)