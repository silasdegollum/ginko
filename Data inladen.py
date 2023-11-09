# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 18:38:52 2023

Dit script geeft wat inzicht in de 100k dataset die MovieLens beschikbaar heeft gesteld.

@author: silas
"""


import pandas as pd

#leuk en alles maar hier staat alleen info over de films zelf in, niet de gebruiker.
df = pd.read_csv(r"C:\Users\silas\Documents\GitHub\ginko\movielens_100k.csv")

#hieronder worden drie dataframes gemaakt met data erin: De ratings die gebruikers van een film hebben gegeven,
#informatie over de gebruikers, en
#informatie over de films.

data = pd.read_csv(r"C:\Users\silas\Documents\GitHub\ginko\ml-100k\ml-100k\u.data", sep='\t', 
                   names=['user id', 'item id', 'rating', 'timestamp'], header=None)
user = pd.read_csv(r"C:\Users\silas\Documents\GitHub\ginko\ml-100k\ml-100k\u.user", sep='\t', 
                   names=['user id', 'age', 'gender', 'occupation', 'zip code'], header=None)

#Dit geeft een foutmelding omdat é niet in de codec staat, megairritant. heb er nog geen oplossing voor.
#item = pd.read_csv(r"C:\Users\silas\Documents\GitHub\ginko\ml-100k\ml-100k\u.item", sep='\t', 
                #   names=['movie id', 'movie title', 'release date', 'video release date', 'IMDB URL', 
                 #         'unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 
                  #        'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 
                   #       'Romance', 'Sci_Fi', 'Thriller', 'War', 'Western'], header=None)

