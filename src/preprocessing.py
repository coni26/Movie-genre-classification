import pandas as pd

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

#Premiers nettoyages

def clean_text(s):
    return s.replace("’"," ").replace("'"," ").replace(".", "").replace(":", "").replace(",","").replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ù","u").replace("û","u").replace("â","a").replace("ç","c").replace("ï","i").replace('…','').replace('(',' ').replace(')',' ').lower().split(" ")

def stem_list(l):
    res = []
    for word in l:
        res.append(stemmer.stem(word))
    return res

#Conversion des genres en vecteurs binaires
def genres_to_vec(l):
    res = [0]*len(dic_genres)
    for genre in literal_eval(l):
        res[dic_genres[genre]]=1
    return res

#Sélection des genres suffisamment représentés
def genres_selection(df):
    for i,row in df.iterrows():
        for genre in literal_eval(row['Genre(s)']):
            if dic_genres[genre]>16: 
                df.drop(i,inplace=True)
                break
    return df

#Suppression de mots Stopwords ou trop récurents
french_stopwords = list(set(stopwords.words('french')))

for i in range(len(french_stopwords)):
    french_stopwords[i] = french_stopwords[i].replace("é","e").replace('é','e').replace("è","e").replace("ê","e").replace("à","a").replace("ù","u").replace("û","u").replace("ü","u").replace("ï",'i').replace("â","a").replace("ç","c").replace("ï","i").replace("î","i")

dic_words = {}
for i, row in df.iterrows():
    for word in row['Synopsis']:
        if len(word)>2:
            if not(word in french_stopwords):
                if word in dic_words:
                    dic_words[word]+=1
                else:
                    dic_words[word]=1
                    
french_stopwords += [k for k,v in dic_words.items() if v>4000]
                    
              
