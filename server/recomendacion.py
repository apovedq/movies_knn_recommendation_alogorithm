#!/usr/bin/env python
import numpy as np
import pandas as pd
import sklearn as sk
from sklearn.cluster import DBSCAN
import sklearn.metrics.pairwise 
class Rec:

    #Inicializa todas las variables base
    def __init__(self):

        # Dataframe con usuarios (a comparar)
        self.df = pd.read_csv('../data/actores.csv')

        # Dataframe con peliculas (recomendaciones)
        self.peliculas = pd.read_csv('../data/peliculas.csv')


        # Usuario selecionado a comparar con dataframe original
        self.user_select = 'Andres Poveda'

        # Usuario agregado, resultado del anterior, a comparar con dataframe de sugerencias
        self.protopersona = 0


        # como crear un dict
        #pesos = {
        #    'Pop': 0.1,
        #    'Indie': 0.1
        #}
        # como agregar vals
        #pesos['Pop'] = 0.1

        # crear diccionario con los pesos de todas las columnas (excepto User)
        self.pesos = {}


        # Iterador del tamaño de la dimension vertical correlacionando cada fila con usuario seleccionado y agregandolo al diccionario
        self.corrs = {}


        # Numero de usuarios a considerar como vecinos cercanos
        self.num_vec = 5

        # Metodo de agrupacion elegido: 
        # 0 = Naive Average, 1 = Least Misery, 2 = Maximum Pleasure, 3 = Media Satisfaction
        self.agr_met = 0


        # Numero de recomendaciones
        self.num_rec = 4

        self.rec_corrs = {}

    ###### SETTERS #####

    # modifica usuario seleccionado

    def set_user_select(self, x):
        self.user_select = x
        print("SET_USER_SELECT: ", self.user_select)


    # coloca arreglo de pesos en orden de columna izq a der
    def set_pesos(self, x):
        cnt = 0;
        for i in self.pesos.keys():
            self.pesos[i] = x[cnt]
            cnt += 1
        print("SET_PESOS: ", self.pesos)


    # asigna num usuarios y metodo de agregacion
    def set_num_vec(self, x):
        if(x>0 and x<self.dfCopy.shape[0]):
            self.num_vec = x
        print("SET_NUM_VEC: ", self.num_vec)

    def set_agr_met(self, x):
        if(x>0 and x<4):
            self.agr_met = x
        print("SET_AGR_MET: ", self.agr_met)


    # asigna num recomendaciones
    def set_num_rec(self, x):
        if(x>0 and x<self.peliculasCopy.shape[0]):
            self.num_rec = x
        print("SET_NUM_REC: ", self.num_rec)

    ##### FUNCIONES ETC #####
    # Obtener top N valores de un diccionario D
    def top_val(self, N, D):
        temp = D.copy()
        final = {}
        
        # iterador que agrega los N valores mas grandes del diccionario al diccionario final
        for i in range(N+1):
            new = list(temp.keys())[list(temp.values()).index(max(temp.values()))]
            final[new] = temp[new]
            temp.pop(new)
        return final

    ##### BLOQUE DE CORRELACION / USUARIOS RECOMENDADOS / VECINDARIOS #####
    def exec(self):

        if (self.pesos == {}):
            for i in self.df.drop(columns='User').columns:
                self.pesos[i] = 1
                
        print("RECOMENDACION PY INICIAL !!!!!!! \n")
        print("INICIO df \n", self.df)
        print("INICIO peliculas \n", self.peliculas)
        print("INICIO user_select \n", self.user_select)
        print("INICIO protopersona \n", self.protopersona)
        print("INICIO pesos \n", self.pesos)
        print("INICIO corrs \n", self.corrs)
        print("INICIO num_vec \n", self.num_vec)
        print("INICIO agr_met \n", self.agr_met)
        print("INICIO num_rec \n", self.num_rec)
        print("INICIO rec_corrs \n", self.rec_corrs)
        
        # Asegurar valores como float
        for i in self.df.drop(columns='User').columns:
            self.df[i] = pd.to_numeric(self.df[i], downcast='float')

        for i in self.peliculas.drop(columns='Movie').columns:
            self.peliculas[i] = pd.to_numeric(self.peliculas[i], downcast='float')


        # copia dataframes
        self.dfCopy = self.df.copy()
        self.peliculasCopy = self.peliculas.copy()


        ## normalizar valores
        self.dfCopy = self.dfCopy.drop(columns="User")
        self.dfCopy = (self.dfCopy-self.dfCopy.min())/(self.dfCopy.max()-self.dfCopy.min())
        self.dfCopy.insert(0, "User", self.df['User'])

        self.peliculasCopy = self.peliculasCopy.drop(columns="Movie")
        self.peliculasCopy = (self.peliculasCopy-self.peliculasCopy.min())/(self.peliculasCopy.max()-self.peliculasCopy.min())
        self.peliculasCopy.insert(0, "Movie", self.peliculas['Movie'])


        # CORRELACION ENTRE USUARIOS

        # multiplica las columnas con su llave respectiva en el diccionario de pesos (Pop con peso de Pop...)
        for i in self.dfCopy.drop(columns="User").columns:
            self.dfCopy[i] = self.dfCopy[i]*self.pesos[i]



        # Como encontrar fila con valor de columna (cuando el User sea igual al usuario)
        # self.dfCopy.loc[self.dfCopy['User']==self.user_select]

        # Lo mismo pero con valor solo conocido por el indice
        # self.dfCopy.loc[self.dfCopy['User']== self.dfCopy.iloc[1].User]

        # Funcion de similitud coseno
        self.cos_sim = sklearn.metrics.pairwise.cosine_similarity


        for i in range(self.dfCopy.shape[0]):
            self.corrs[self.dfCopy.iloc[i].User] = self.cos_sim(self.dfCopy.loc[self.dfCopy['User']==self.user_select].drop(columns='User') , self.dfCopy.loc[self.dfCopy['User']==self.dfCopy.iloc[i].User].drop(columns='User'))[0][0] 



        # Vecindarios

        self.vecinos = self.top_val(self.num_vec, self.corrs)

        # borra el usuario seleccionado
        self.vecinos.pop(self.user_select)


    ##### BLOQUE DE AGREGACION / PROTOPERSONA / RECOMENDACION FINAL #####
        # AGREGACION
        # dataframe vacio
        self.protopersona = pd.DataFrame(data=None, columns=self.dfCopy.drop(columns='User').columns)

        # primer fila en 0
        self.protopersona.loc[len(self.protopersona)] = 0


        # obtiene los dataframes de las personas en el diccionario vecinos y los une en la protopersona
        for i in self.vecinos.keys():
            self.dfI = self.dfCopy.loc[self.dfCopy['User']==i].drop(columns='User')
            self.protopersona = self.protopersona.add(self.dfI, fill_value=0)

        self.protopersona = self.protopersona.drop(0)


        # guardemos protopersona sin tocar
        self.protoCopy = self.protopersona.copy()


        # Aplica metodo
        # 0 = Naive Average, 1 = Least Misery, 2 = Maximum Pleasure, 3 = Media Satisfaction
        self.agr_met = 0

        if (self.agr_met == 0):
            # se deja el promedio
            self.protoCopy = self.protoCopy.mean()
            
        elif (self.agr_met == 1):
            # se borran columnas menores de 0.5
            self.protoCopy = self.protoCopy.mean()
            for i in self.protoCopy.keys():
                if(self.protoCopy[i] < 0.5):
                    self.protoCopy[i] = 0
                    
        elif (self.agr_met == 2):
            # se borran columnas menores de 0.8
            self.protoCopy = self.protoCopy.mean()
            for i in self.protoCopy.keys():
                if(self.protoCopy[i] < 0.8):
                    self.protoCopy[i] = 0
            
        elif (self.agr_met == 3):
            # se dejan las desviaciones estandar bajas
            
            # arreglo de columnas a "borrar"
            remove = []
            
            for col in self.protoCopy.columns:
                # si la columna no tiene la minima desviacion, agregar a arreglo
                if(self.protoCopy[col].std().min() != self.protoCopy.std().min()):
                    remove.append(col)
                    
            # borrar las columnas en arreglo
            self.protoCopy[remove[:]] = 0
            
            # ahora si promediamos
            self.protoCopy = self.protoCopy.mean()

        else:
            print('wrong number: 0 = Naive Average, 1 = Least Misery, 2 = Maximum Pleasure, 3 = Media Satisfaction')
            

        # convertimos usuario a dataframe
        self.protoCopy = self.protoCopy.to_frame()

        # lo rotamos para que este en el formato correcto
        self.protoCopy = self.protoCopy.transpose()


        # RECOMENDACION
        # Correlacion
        for i in range(self.peliculasCopy.shape[0]):
            self.rec_corrs[self.peliculasCopy.iloc[i].Movie] = self.cos_sim(self.protoCopy , self.peliculasCopy.loc[self.peliculasCopy['Movie']==self.peliculasCopy.iloc[i].Movie].drop(columns='Movie'))[0][0] 


        # Vecindarios
        self.num_rec = self.num_rec -1

        self.recomendaciones = self.top_val(self.num_rec, self.rec_corrs)


        # dataframe con todas las recomendaciones y sus valores junto a la protopersona
        # dataframe vacio
        self.final_rec = pd.DataFrame(data=None, columns=self.dfCopy.rename(columns={'User':'Name'}).columns)

        # primer fila en 0
        self.final_rec.loc[len(self.final_rec)] = 0


        # obtiene los dataframes de las recomendaciones y la protopersona
        self.dfs = []
        for i in self.recomendaciones.keys():
            self.dfs.append(self.peliculasCopy.loc[self.peliculasCopy['Movie']==i].rename(columns={'Movie':'Name'}))

        self.dfs.append(self.protoCopy)
        self.dfs[len(self.dfs)-1].insert(0, 'Name', 'Protopersona')
        self.final_rec = pd.concat(self.dfs)


        print("RECOMENDACION PY FINAL /////// \n")
        print("FINAL user_select \n", self.user_select)
        print("FINAL protopersona \n", self.protopersona)
        print("FINAL pesos \n", self.pesos)
        print("FINAL corrs \n", self.corrs)
        print("FINAL num_vec \n", self.num_vec)
        print("FINAL vecinos \n", self.vecinos)
        print("FINAL agr_met \n", self.agr_met)
        print("FINAL num_rec \n", self.num_rec)
        print("FINAL rec_corrs \n", self.rec_corrs)
        print("FINAL PY \n", self.final_rec)

    ##### GETTERS #####

    ### Resultado final del codigo 
    def get_final_dataframe(self):
        return self.final_rec


    def get_corr_protopersona(self):
        return self.rec_corrs

    def get_recomendaciones(self):
        return self.recomendaciones

    def get_num_rec(self):
        return self.num_rec

    def get_vecinos(self):
        return self.vecinos

    def get_vecindario_df(self):
        return self.protopersona

    def get_protopersona(self):
        return self.protoCopy

    def get_num_vec(self):
        return self.num_vec

    def get_agr_met(self):
        return self.agr_met

    def get_norm_df(self):
        return self.dfCopy

    def get_corrs(self):
        return self.corrs

    def get_pesos(self):
        return self.pesos

    def get_main_df(self):
        return self.df

    def get_recommend_df(self):
        return self.peliculas

    def get_user_select(self):
        return self.user_select

    def get_user_list(self):
        return self.dfCopy["User"].to_list();

    ##### REINICIA ####
    def reset(self):
        self.final_rec = 0;
        self.df = pd.read_csv('../data/actores.csv')
        self.peliculas = pd.read_csv('../data/peliculas.csv')
        self.user_select = 'Andres Poveda'
        self.protopersona = 0
        self.pesos = {}
        self.corrs = {}
        self.num_vec = 5
        self.agr_met = 0
        self.num_rec = 4
        self.rec_corrs = {}
