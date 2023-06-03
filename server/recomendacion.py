#!/usr/bin/env python
# coding: utf-8

# # SISTEMA DE RECOMENDACION USANDO AGRUPACION Y KNN

# ## TRATAMIENTO DE DATOS

# In[11]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.cluster import DBSCAN


# In[12]:


df = pd.read_csv('../data/actores.csv')
df.head()


# In[13]:


df.describe()


# In[14]:


df.columns


# In[15]:


# dataframe con las recomendaciones de peliculas
peliculas = pd.read_csv('../data/peliculas.csv')
peliculas.head()


# In[16]:


peliculas


# In[17]:


# retorna dataframes sin modificar

def get_main_df():
    return df

def get_recommend_df():
    return peliculas


# In[18]:


# Usuario selecionado a comparar con dataframe original
user_select = 'Sebastian Mosquera'

# Usuario agregado, resultado del anterior, a comparar con dataframe de sugerencias
protopersona = 0


# In[19]:


# Retorna o modifica usuario seleccionado

def get_user_select():
    return user_select

def set_user_select(x):
    user_select = x
    return 1


# In[20]:


# como crear un dict
pesos = {
    'Pop': 0.1,
    'Indie': 0.1
}
# como agregar vals
pesos['Pop'] = 0.1



# crear diccionario con los pesos de todas las columnas (excepto User)
pesos = {}

for i in df.drop(columns='User').columns:
        pesos[i] = 1
        
print(pesos)


# In[21]:


# Retornar o cambiar dict de pesos
def get_pesos():
    return pesos

def set_pesos(x):
    pesos = x
    return 1


# In[22]:


# Asegurar valores como float

for i in df.drop(columns='User').columns:
    df[i] = pd.to_numeric(df[i], downcast='float')

for i in peliculas.drop(columns='Movie').columns:
    peliculas[i] = pd.to_numeric(peliculas[i], downcast='float')


# In[23]:


print(type(df['Tim Burton'][0]))


# In[24]:


# copia dataframes

dfCopy = df.copy()
peliculasCopy = peliculas.copy()


# In[25]:


## normalizar valores

# solucion satanica
dfCopy = dfCopy.drop(columns="User")
dfCopy = (dfCopy-dfCopy.min())/(dfCopy.max()-dfCopy.min())
dfCopy.insert(0, "User", df['User'])

peliculasCopy = peliculasCopy.drop(columns="Movie")
peliculasCopy = (peliculasCopy-peliculasCopy.min())/(peliculasCopy.max()-peliculasCopy.min())
peliculasCopy.insert(0, "Movie", peliculas['Movie'])


# ## CORRELACION ENTRE USUARIOS

# #### Aplicacion de pesos

# In[26]:


# multiplica las columnas con su llave respectiva en el diccionario de pesos (Pop con peso de Pop...)
for i in dfCopy.drop(columns="User").columns:
    dfCopy[i] = dfCopy[i]*pesos[i]


# In[27]:


# retorna dataframe normalizado
def get_norm_df():
    return dfCopy


# #### Correlacion

# In[28]:


import sklearn.metrics.pairwise 


# In[29]:


# Como encontrar fila con valor de columna (cuando el User sea igual al usuario)
dfCopy.loc[dfCopy['User']==user_select]

# Lo mismo pero con valor solo conocido por el indice
dfCopy.loc[dfCopy['User']== dfCopy.iloc[1].User]

# Funcion de similitud coseno
cos_sim = sklearn.metrics.pairwise.cosine_similarity

# Iterador del tamaño de la dimension vertical correlacionando cada fila con usuario seleccionado y agregandolo al diccionario
corrs = {}

for i in range(dfCopy.shape[0]):
    corrs[dfCopy.iloc[i].User] = cos_sim(dfCopy.loc[dfCopy['User']==user_select].drop(columns='User') , 
                                                                          dfCopy.loc[dfCopy['User']==dfCopy.iloc[i].User].drop(columns='User'))[0][0] 
print(corrs)


# In[30]:


# retorna diccionario de correlaciones con usuario seleccionado
def get_corrs():
    return corrs


# #### Vecindarios

# In[31]:


# Numero de usuarios a considerar como vecinos cercanos
num_vec = 5

# Metodo de agrupacion elegido: 0 = Naive Average, 1 = Least Misery, 2 = Maximum Pleasure, 3 = Media Satisfaction

agr_met = 0


# In[32]:


# retorna y signa num usuarios y metodo

def get_num_vec():
    return num_vec

def get_agr_met():
    return agr_met

def set_num_vec(x):
    if(x>0 and x<dfCopy.shape[0]):
        num_vec = x
        return 1
    else:
        return 0

def set_agr_met(x):
    if(x>0 and x<4):
        agr_met = x
        return 1
    else:
        return 0


# In[33]:


# Obtener top N valores de un diccionario D
def top_val(N, D):
    temp = D.copy()
    final = {}
    
    # animal satanico para obtener llave con un valor, en este caso, el valor maximo
    # print(list(temp.keys())[list(temp.values()).index(max(temp.values()))])
    
    # iterador que agrega los N valores mas grandes del diccionario al diccionario final
    
    for i in range(N+1):
        new = list(temp.keys())[list(temp.values()).index(max(temp.values()))]
        final[new] = temp[new]
        temp.pop(new)
    return final


# In[34]:


vecinos = top_val(num_vec, corrs)

# borra el usuario seleccionado
vecinos.pop(user_select)

print(vecinos)


# In[35]:


# Retorna vecinos
def get_vecinos():
    return vecinos


# ## AGREGACION

# #### crear protopersona

# In[36]:


# dataframe vacio
protopersona = pd.DataFrame(data=None, columns=dfCopy.drop(columns='User').columns)
# primer fila en 0
protopersona.loc[len(protopersona)] = 0


# In[37]:


# obtiene los dataframes de las personas en el diccionario vecinos y los une en la protopersona
for i in vecinos.keys():
    dfI = dfCopy.loc[dfCopy['User']==i].drop(columns='User')
    protopersona = protopersona.add(dfI, fill_value=0)

protopersona = protopersona.drop(0)
print(protopersona)


# In[38]:


# retornar dataframe de vecindario
def get_vecindario_df():
    return protopersona


# In[39]:


# guardemos protopersona sin tocar
protoCopy = protopersona.copy()


# #### Aplica metodo

# In[40]:


# 0 = Naive Average, 1 = Least Misery, 2 = Maximum Pleasure, 3 = Media Satisfaction
agr_met = 0

if (agr_met == 0):
    # se deja el promedio
    protoCopy = protoCopy.mean()
    
elif (agr_met == 1):
    # se borran columnas menores de 0.5
    protoCopy = protoCopy.mean()
    for i in protoCopy.keys():
        if(protoCopy[i] < 0.5):
            protoCopy[i] = 0
            
elif (agr_met == 2):
    # se borran columnas menores de 0.8
    protoCopy = protoCopy.mean()
    for i in protoCopy.keys():
        if(protoCopy[i] < 0.8):
            protoCopy[i] = 0
    
elif (agr_met == 3):
    # se dejan las desviaciones estandar bajas
    
    # arreglo de columnas a "borrar"
    remove = []
    
    for col in protoCopy.columns:
        # si la columna no tiene la minima desviacion, agregar a arreglo
        if(protoCopy[col].std().min() != protoCopy.std().min()):
            remove.append(col)
            
    # borrar las columnas en arreglo
    protoCopy[remove[:]] = 0
    
    # ahora si promediamos
    protoCopy = protoCopy.mean()

else:
    print('wrong number: 0 = Naive Average, 1 = Least Misery, 2 = Maximum Pleasure, 3 = Media Satisfaction')
    
# convertimos usuario a dataframe
protoCopy = protoCopy.to_frame()

# lo rotamos para que este en el formato correcto
protoCopy = protoCopy.transpose()

print(protoCopy)


# In[41]:


protoCopy.head()


# In[42]:


# retornar protopersona final
def get_protopersona():
    return protoCopy


# ## RECOMENDACION

# Ahora creamos un vecindario de la protopersona con los perfiles a recomendar, y a la final le recomendamos los mas parecidos... es repetir el paso de correlacion y vecindarios pero con el otro dataframe y en ves de la persona elegida, la protopersona

# #### Correlacion

# In[43]:


# Numero de recomendaciones
num_rec = 4


# In[44]:


# retorna y asigna num recomendaciones

def get_num_rec():
    return num_rec

def set_num_rec(x):
    if(x>0 and x<peliculasCopy.shape[0]):
        num_vec = x
        return 1
    else:
        return 0


# In[45]:


rec_corrs = {}


for i in range(peliculasCopy.shape[0]):
    rec_corrs[peliculasCopy.iloc[i].Movie] = cos_sim(protoCopy , peliculasCopy.loc[peliculasCopy['Movie']==peliculasCopy.iloc[i].Movie].drop(columns='Movie'))[0][0] 
print(rec_corrs)


# In[46]:


# retorna nivel de correlacion con dataframe de correlacion
def get_corr_protopersona():
    return rec_corrs


# #### Vecindarios

# In[47]:


# aqui no tenemos usuario repetido...
num_rec = num_rec -1

recomendaciones = top_val(num_rec, rec_corrs)

print(recomendaciones)


# In[48]:


# !HHHHHechioho!
# retorna las recomendaciones finales
def get_recomendaciones():
    return recomendaciones


# #### dataframe con todas las recomendaciones y sus valores junto a la protopersona

# In[49]:


# dataframe vacio
final_rec = pd.DataFrame(data=None, columns=dfCopy.rename(columns={'User':'Name'}).columns)
# primer fila en 0
final_rec.loc[len(final_rec)] = 0


# In[50]:


# obtiene los dataframes de las recomendaciones y la protopersona
dfs = []
for i in recomendaciones.keys():
    dfs.append(peliculasCopy.loc[peliculasCopy['Movie']==i].rename(columns={'Movie':'Name'}))

dfs.append(protoCopy)
print(dfs[len(dfs)-1])
dfs[len(dfs)-1].insert(0, 'Name', 'Protopersona')
print(dfs[len(dfs)-1])
final_rec = pd.concat(dfs)
#print(final_rec)


# In[51]:


final_rec.head()


# In[52]:


def get_final_dataframe():
    return final_rec


# In[ ]:




