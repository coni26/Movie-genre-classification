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
