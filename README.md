# Movie genre classification
L'objectif de ce projet est de tenter de répondre à la question suivante : peut-on prédire le(s) genre(s) d'un film à partir de son synopsis ?
Pour ce faire, nous avons construit une base de données à partir de films (titre, genre(s), synopsis) récupérés sur Allociné. Après avoir visualisé les données à travers différents paramètres, nous avons utilisé plusieurs modèles que nous comparons pour tenter de trouver celui nous permettant de répondre au mieux à cette question. 
Notre modèle final étant une régression logistic multi_label

## Table des matières
  * Webscraping d'Allociné
  * Visualisation et préprocessing
  * Modélisation
  
## I. Webscraping d'Allociné
Nous avons récupérer les données sur [Allociné](http://allocine.fr). Le processus peut être assez long, c'est pourquoi nous proposons de tester les algorithmes sur un faible nombre de données. En réalité, nous avons scrapté plus de 20.000 films.

## II. Visualisation et préprocessing
A l'aide de différents graphes, nous expliquons notre stratégie de sélection des variables 
