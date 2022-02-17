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

word = "septuple"
try:
    url = f"https://fr.wiktionary.org/wiki/{word}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    s = soup.find("ol").find_all("li")
    ss = s[0].getText()
    if "personne du" in ss.lower():
        try:
            print(s[0].find("a")["href"])
            url = "https://fr.wiktionary.org" + s[0].find("a")["href"]
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            sss = soup.find("ol").find_all("li")
            print(sss[0].getText().split("\n")[0])
        except:
            #print(ss)
            pass
    print(s[0].getText())
except:
    print("Zé pas trouvé désolé")


