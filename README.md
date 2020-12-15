# Movie genre classification
L'objectif de ce projet est de tenter de répondre à la question suivante : peut-on prédire le(s) genre(s) d'un film à partir de son synopsis ?

## Table des matières
  * Webscraping d'Allociné
  * Visualisation et préprocessing
  * Modélisation
  
## I. Webscraping d'Allociné
Nous avons consitué une base de données grâce au site [Allociné](http://allocine.fr) en récupérant le titre, le synopsis et le(s) genre(s) de 22000 films. Nous avons aussi pris comme décision de ne sélectionner que les films ayant un synopsis assez long pour être étudié, c'est-à-dire d'un nombre de caractères supérieur à 250.

## II. Visualisation et préprocessing
 * Visualisation sur les genres : nous regardons le nombre de films appartenant à chacun des genres mais aussi les liens entre les genres grâce aux films multi-genres.
 * Visualisation sur les mots : nous étudions le champ lexical des synopsis en fonction des genres, pour voir s'il y a des différences directement visibles


## III. Modélisation
Notre tâche consistait à réaliser une classification multi-label. 
Pour cela nous avons d'abord étudier différents algorithmes de classification binaire :

 * SVC
 * Random Forest
 * Logistic Regression
 
Puis en observant que la régression logistique était la plus appropriée nous avons construit un algortihme de classification multi-label en empilant des Logistic Regression en Stacking Structure.

Enfin nous comparons ce modèle à un réseau de neurones.
