import pandas as pd
import numpy as np

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()

from ast import literal_eval


dic_genres = {'Drame': 0,
              'Comédie': 1,
              'Thriller': 2,
              'Action': 3,
              'Romance': 4,
              'Comédie dramatique': 5,
              'Documentaire': 6,
              'Aventure': 7,
              'Policier': 8,
              'Epouvante-horreur': 9,
              'Fantastique': 10,
              'Animation': 11,
              'Science fiction': 12,
              'Famille': 13,
              'Historique': 14,
              'Biopic': 15,
              'Guerre': 16,
              'Musical': 17,
              'Western': 18,
              'Divers': 19,
              'Erotique': 20,
              'Comédie musicale': 21,
              'Espionnage': 22,
              'Arts Martiaux': 23,
              'Judiciaire': 24,
              'Sport event': 25,
              'Bollywood': 26,
              'Expérimental': 27,
              'Péplum': 28,
              'Concert': 29,
              'Opera': 30,
              'Show': 31,
              'Drama': 32,
              'Dessin animé': 33}


def clean_text(s):
    return s.replace("’"," ").replace("'"," ").replace(".", "").replace(":", "").replace(",","").replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ù","u").replace("û","u").replace("â","a").replace("ç","c").replace("ï","i").replace('…','').replace('(',' ').replace(')',' ').lower().split(" ")

def stem_list(l):
    res = []
    for word in l:
        res.append(stemmer.stem(word))
    return res


def genres_to_vec(l):
  '''
    Conversion des genres en dummy vecteur
  '''
    res = [0]*len(dic_genres)
    for genre in literal_eval(l):
        res[dic_genres[genre]]=1
    return res

def genres_selection(df):
    for i,row in df.iterrows():
        for genre in literal_eval(row['Genre(s)']):
            if dic_genres[genre]>16: 
                df.drop(i,inplace=True)
                break
    return df

                    
  
def ban_words(df, limit_inf=10, limit_sup=np.inf):
    
    french_stopwords = list(set(stopwords.words('french')))
    banned_words = []

    for word in french_stopwords:
        word = word.replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ù","u").replace("û","u").replace("ç","c").replace("ï","i")
        banned_words.append(stemmer.stem(word))

    dic = {}

    for i, row in df.iterrows():
        l = row['Synopsis']
        for k, word in enumerate(l):
            if len(word)<=2:
                continue
            if not(word in l[:k]):
                if word in dic:
                    dic[word]+=1
                else:
                    dic[word]=1

    banned_words += [k for k,v in dic.items() if (v<=limit_inf or v>limit_sup)]
    return banned_words
              
