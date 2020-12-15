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


def histogramme(df):
  dic_nb_genres = {}

  for i, row in df.iterrows():
      for genre in literal_eval(row['Genre(s)']):
          if genre in dic_nb_genres:
              dic_nb_genres[genre] += 1
          else:
              dic_nb_genres[genre] = 1

  dic_nb_genres = {k: v for k, v in sorted(dic_nb_genres.items(), key=lambda item: item[1], reverse=False)}
  plt.figure(figsize=(10, 10))
  colors = ['r'] * 17 + ['steelblue'] * 17
  plt.barh(list(dic_nb_genres.keys()), dic_nb_genres.values(), color=colors)
  plt.title('Répartition des films par genre')
  plt.xlabel('Nombre de films')
  plt.show()

  
def reseau_genres(df, dic_genres):
  '''
      Représentation des liens entre les genres sous forme de réseau
  '''
  mat = np.zeros((17,17), dtype=int)

  for _, row in df.iterrows():
      genres = literal_eval(row['Genre(s)'])
      for i in range(len(genres)):
          for j in range(i,len(genres)):
              x = dic_genres[genres[i]]
              y = dic_genres[genres[j]]
              if x>y :
                  x, y = y, x
              mat[x,y] += 1

  plt.figure(figsize=(15,12))

  G = nx.Graph()
  for i in range(16):
      for j in range(i+1,17):
          G.add_edge(i,j,color='r',weight=mat[i,j]/150)

  pos = nx.circular_layout(G)

  edges = G.edges() 
  colors = [G[u][v]['color'] for u,v in edges]
  weights = [G[u][v]['weight'] for u,v in edges]
  node_size = [mat[i,i]/1.5 for i in range(17)]

  options = {"alpha": 0.6}
  nx.draw_networkx_nodes(G, pos, node_color="steelblue", node_size=node_size, **options)

  nx.draw_networkx_edges(G, pos, edge_color=colors, width=weights)

  labels = {}
  labels[0] = 'Drame'
  labels[1] = 'Comédie'
  labels[2] = 'Thriller'
  labels[3] = 'Action'
  labels[4] = 'Romance'
  labels[5] = 'Comédie dramatique'
  labels[6] = 'Documentaire'
  labels[7] = 'Aventure'
  labels[8] = 'Policier'
  labels[9] = 'Epouvante'
  labels[10] = 'Fantastique'
  labels[11] = 'Animation'
  labels[12] = 'Science fiction'
  labels[13] = 'Famille'
  labels[14] = 'Historique'
  labels[15] = 'Biopic'
  labels[16] = 'Guerre'

  nx.draw_networkx_labels(G, pos, labels, font_size=16)
  plt.show()



def words_genre(df, dic_genres):
  l_dico = []
  for k in range (17):
      l_dico.append({})

  for i, row in df.iterrows():
      l = row['Synopsis']
      lst = []
      for genre in literal_eval(row['Genre(s)']):
          if dic_genres[genre]<=16 : 
              lst.append(dic_genres[genre])
      for k, word in enumerate(l):
          if not((len(word)<=2) or (word in french_stopwords) or (word in l[:k])):
              for p in lst:
                  if word in l_dico[p]:
                      l_dico[p][word] += 1
                  else:
                      l_dico[p][word] = 1
  return l_dico
                    
def world_cloud_mask(l_dico, num_genre, path):
    mask = np.array(Image.open(path))
    genre = [k  for (k, val) in dic_genres.items() if val == num_genre]
    wordcloud = WordCloud(background_color='white', mask = mask,
                          width=mask.shape[1],
                          height=mask.shape[0]
                          ).generate_from_frequencies(l_dico[num_genre])

    plt.figure(figsize=(15,15))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title('Nuage de mots pour le genre '+'"'+genre[0]+'"', fontsize=20)
    plt.axis('off')
    plt.show()



def draw_Zipf(df) : 
  dic_words_zipf = {}
  for i, row in df.iterrows():
    for word in row['Synopsis']:
        if len(word)>1:
            if word in dic_words_zipf:
                dic_words_zipf[word]+=1
            else:
                dic_words_zipf[word]=1
                
  l_occur = sorted(list((dic_words_zipf.values())), reverse=True)
  lx = [i for i in range(len(l_occur))]
  plt.figure(figsize=(12,8))
  plt.xscale('log')
  plt.yscale('log')
  plt.plot(lx,l_occur,'r+')
  plt.xlabel('Rang du mot')
  plt.ylabel('Fréquence du mot')
  plt.title('Loi de Zipf')
  plt.show()
