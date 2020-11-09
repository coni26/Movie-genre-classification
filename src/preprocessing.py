import pandas as pd



def clean_text(s):
    return s.replace("’"," ").replace("'"," ").replace(".", "").replace(":", "").replace(",","").replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ù","u").replace("û","u").replace("â","a").replace("ç","c").replace("ï","i").replace('…','').replace('(',' ').replace(')',' ').lower().split(" ")

def stem_list(l):
    res = []
    for word in l:
        res.append(stemmer.stem(word))
    return res


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

def genres_to_vec(l):
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
