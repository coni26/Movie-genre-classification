import pandas as pd



def clean_text(s):
    return s.replace("’"," ").replace("'"," ").replace(".", "").replace(":", "").replace(",","").replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ù","u").replace("û","u").replace("â","a").replace("ç","c").replace("ï","i").replace('…','').replace('(',' ').replace(')',' ').lower().split(" ")

def stem_list(l):
    res = []
    for word in l:
        res.append(stemmer.stem(word))
    return res


dic_genres = {'Drame': 0,
              'Comédie dramatique': 1,
              'Comédie': 2,
              'Policier': 3,
              'Romance': 4,
              'Thriller': 5,
              'Aventure': 6,
              'Fantastique': 7,
              'Epouvante-horreur': 8,
              'Action': 9,
              'Documentaire': 10,
              'Historique': 11,
              'Science fiction': 12,
              'Western': 13,
              'Guerre': 14,
              'Musical': 15,
              'Biopic': 16,
              'Animation': 17,
              'Famille': 18,
              'Comédie musicale': 19,
              'Divers': 20,
              'Espionnage': 21,
              'Judiciaire': 22,
              'Erotique': 23,
              'Expérimental': 24,
              'Arts Martiaux': 25,
              'Bollywood': 26,
              'Sport event': 27,
              'Concert': 28,
              'Péplum': 29,
              'Opera': 30,
              'Dessin animé': 31,
              'Show': 32}

def genres_to_vec(l):
    res = [0]*len(dic_genres)
    for genre in literal_eval(l):
        res[dic_genres[genre]]=1
    return res

