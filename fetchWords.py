import requests

words_list = requests.get("https://raw.githubusercontent.com/atebits/Words/master/Words/fr.txt").text

words_list = filter(lambda x: len(x) > 4, words_list.split('\n'))

path = input("Chemin d'écriture ? (words.txt) ")

if path == "":
    path = "./words.txt"

with open(path, "w", encoding="utf-8") as file:
    file.write('\n'.join(words_list))