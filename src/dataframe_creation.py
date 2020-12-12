from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from IPython.display import clear_output
import time

#Liste des identifiants dont l'url correpond bien à un film sur Allociné
#Construction liste
f = open("liste.txt","a") 
for i in range(0,10):
    page = 'https://www.allocine.fr/films/?page='+str(i)
    resp = requests.get(page).text
    soup = BeautifulSoup(resp, 'html.parser')
    for a in soup.find_all('a', href=True):
        if a['href'][:25]=='/film/fichefilm_gen_cfilm':
            f.write((a['href'][26:-5]) + "\n")
f.close()

#Utilisation liste
f= open("liste.txt","r")
l = f.readlines()
f.close()

for i in range(len(l)):
    l[i]=int(l[i][:-1])
    
l = sorted(list(set(l)))

#Webscraping
def create_dataframe(n):
    donnees = []
    i = 0
    start = time.time()
    while len(donnees) < n: 
        if len(donnees)>=1 and (len(donnees)/n)*1000==int((len(donnees)/n)*1000):
            delta = time.time() - start
            clear_output(wait=True)
            minutes = int(delta*(n-len(donnees))/len(donnees)//60)
            secondes = int(delta*(n-len(donnees))/len(donnees)%60)
            print(round((len(donnees)/n)*100,2), '%'
                  , 'Estimated time remaining :', minutes, 'minutes and ', secondes, 'seconds')
        i+=1
        page = 'http://www.allocine.fr/film/fichefilm_gen_cfilm='+str(l[i])+'.html'
        resp = requests.get(page).text
        soup = BeautifulSoup(resp, 'html.parser')
        title = soup.find("div", {"class":"titlebar-title titlebar-title-lg"})
        if title == None: 
            continue
        else :
            section = soup.find("section", {"class": "section ovw ovw-synopsis"})
            synopsis = section.find("div", {"class":"content-txt"})
            if synopsis==None: 
                continue
            synopsis = synopsis.text.strip()
            if len(synopsis)<250:
                continue
            genres = soup.find_all("span", {"class" : lambda value: value and value.startswith("ACrL2ZACrpbG1zL2")})
            genres_multi = []
            for ele in genres: 
                genres_multi.append(ele.text.strip())
            donnees.append([title.text.strip(),synopsis,genres_multi])
    df = pd.DataFrame(donnees, columns=['Titre', 'Synopsis','Genre(s)'])
    clear_output(wait=True)
    print('Création achevée')
    return df, i
