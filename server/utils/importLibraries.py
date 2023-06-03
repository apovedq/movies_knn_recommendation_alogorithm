import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import seaborn as sb
import random

#2. Read the two diferent data sets.

##Todos los usuarios y sus preferencias del 1 al 10 en actores.
recommendation_df = pd.read_csv('./data/actores.csv')

##Todas las peliculas que contienen a cada uno de los personajes, si lo contiene es 10 y sino es 0
movie_selector_df = pd.read_csv('./data/peliculas.csv')


#----------------------------------------------------------------------------------------------------------------------------
#3. Setup widgets
# dropdown: selected user.
selected_user = "Andres Poveda"
# Input: neighboors.
k_neighbors = 5


#3. Display widget

