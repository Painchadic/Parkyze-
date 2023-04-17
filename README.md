# Parkyze
Ce programme permet de générer un parking automatiquement en utilisant des classes et des fonctions Python.

## Installation
Avant de pouvoir utiliser ce script, il est nécessaire d'installer certaines librairies Python. Vous pouvez le faire en exécutant la commande suivante dans votre terminal :

```python
pip install numpy matplotlib shapely
```

## Utilisation
Pour utiliser ce script, vous devez importer le module parkyzeClass ainsi que les librairies suivantes :

```python
import matplotlib.pyplot as plt
import math as m
import parkyzeClass as pc
import numpy as np
import shapely.geometry
import random
```
## Fonctions disponibles
Le script propose les fonctions suivantes :

- remplissageAutoParkingStandard1
Cette fonction permet de générer un parking en forme de U avec une rampe à une extrémité.
La fonction retourne une liste d'instances de la classe Place représentant les places de stationnement.

- remplissageAutoParkingStandard2
Cette fonction permet de générer un parking en forme de L avec une rampe à une extrémité. Les paramètres d'entrée sont les mêmes que pour la fonction remplissageAutoParkingStandard1.
    La fonction retourne une liste d'instances de la classe Place représentant les places de stationnement.

- remplissageAutoParkingStandard3
Cette fonction permet de générer un parking en forme de U avec une rampe à une extrémité et une aire de stationnement à l'autre extrémité. Les paramètres d'entrée sont les mêmes que pour la fonction remplissageAutoParkingStandard1.
    La fonction retourne une liste d'instances de la classe Place représentant les places de stationnement.

- remplissageAutoParkingStandard4
Cette fonction remplit le parking avec des places de parking standard en suivant un schéma de lignes brisées (zigzag).

- remplissageAleatoire 
Cette fonction remplit le parking de manière aléatoire.

- remplissageAutomatique2 
Cette fonction remplit le parking en utilisant un algorithme génétique pour trouver la meilleure configuration possible.

Des fonctions auxiliaires pour les fonctions de remplissage :

- remplissageAleatoireAux qui est utilisée par remplissageAleatoire pour remplir le parking de manière aléatoire.
- remplissageAutomatiqueAux2 qui est utilisée par remplissageAutomatique2 pour implémenter l'algorithme génétique.


Les paramètres pour chaque fonction sont les suivants :

> - Parking : une instance de la classe Parking représentant le parking.
- espace : une liste de points représentant l'espace de travail.
- rampe : une instance de la classe Rampe représentant la rampe d'accès au parking.
- largeurRoute : la largeur des routes dans le parking.
- longueurPlace : la longueur des places de parking dans le parking.
- largeurPlace : la largeur des places de parking dans le parking.
- generations : le nombre de générations à utiliser pour l'algorithme génétique (pour remplissageAutomatique2).
- nombreDeFils : le nombre de descendants pour chaque génération de l'algorithme génétique (pour remplissageAutomatique2).
- nombreDeSurvivant : le nombre de survivants pour chaque génération de l'algorithme génétique (pour remplissageAutomatique2).


## Exemple d'utilisation
Voici un exemple d'utilisation de la fonction remplissageAutoParkingStandard1 :

```python
espace = pc.EspaceDeTravail([(-20,-70), (-20,20), (30,20), (30,-70), (-20,-70)])
rampe = pc.Rampe(14, 5, [-25,10], 0, 2)
places = remplissageAutoParkingStandard1(espace, rampe, 5, 6, 2)
for place in places:
    place.plot()
plt.show()
```
Cet exemple génère un parking en forme de U avec une rampe à une extrémité, une largeur de route de 5, une longueur de place de 6 et une largeur de place de 2. Il affiche ensuite le parking à l'aide de la librairie Matplotlib.


>Le programme peut être exécuté en utilisant la commande `python parkyze.py`. Les résultats sont affichés sur la console et une visualisation graphique du parking est générée à l'aide de la bibliothèque pygame.
