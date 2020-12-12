#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[ ]:


dic_nb_genres = {}

for i, row in df.iterrows():
    for genre in literal_eval(row['Genre(s)']):
        if genre in dic_nb_genres:
            dic_nb_genres[genre] += 1
        else:
            dic_nb_genres[genre] = 1


# In[ ]:


dic_nb_genres = {k: v for k, v in sorted(dic_nb_genres.items(), key=lambda item: item[1], reverse=False)}
plt.figure(figsize=(10, 10))
colors = ['r'] * 17 + ['steelblue'] * 17
plt.barh(list(dic_nb_genres.keys()), dic_nb_genres.values(), color=colors)
plt.title('Répartition des films par genre')
plt.xlabel('Nombre de films')
plt.show()
