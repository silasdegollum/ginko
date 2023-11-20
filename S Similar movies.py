# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 14:38:55 2023
@author: silas

Dit is een uitwerking van de volgende tutorial:
    https://towardsdatascience.com/item-based-collaborative-filtering-in-python-91f747200fab
Gebaseerd op de 25M dataset van MovieLens. 
Je kan op dit moment alleen nog maar een filmnummer invoegen, en het filteren is enkel gebaseerd op de rating.
Hier heb je dus nog niet heel veel aan.

"""

import pandas as pd
import numpy as np

#filmdata inladen en de genres elk in een eigen kolom zetten.
movies = pd.read_csv(r"C:\Users\silas\Documents\HU\5Minor\Periode 2\Data\ml-25m\ml-25m\movies.csv")
genres = movies['genres'].str.split('|', expand=True)              #Deze split de genres in hun eigen deel
dummies = pd.get_dummies(genres[0])                                #Deze tovert het weer om in alle genres en binair of een film ze bezit
del movies['genres']
movies = pd.concat([movies, dummies], axis=1)                      #Dit voegt de kolommen bij de eerste dataset
#movies = movies.set_index('movieId')       Dit moet voor nu even uit staan, anders klopt de lookup niet.


#rating data inladen
rating = pd.read_csv(r"C:\Users\silas\Documents\HU\5Minor\Periode 2\Data\ml-25m\ml-25m\ratings.csv").astype(float)
rating[['userId', 'movieId', 'timestamp']] = rating[['userId', 'movieId', 'timestamp']].astype(int)

#Een kleinere dataset maken en deze in een pivot table zetten
rating_klein = rating[rating['movieId']<=200]
matrix = rating_klein.pivot_table(values='rating', index='movieId', columns='userId', fill_value=0)



#De inputs voor het programma. Je moet een indexnummer invoegen
movie_to_select = int(input('What movie do you want to compare to?'))
amount_of_recommendations = 5+1                 #Dit moet omdat de nearest neigbor de film zelf is. Hij raadt dus 5 films aan.

from sklearn.neighbors import NearestNeighbors
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(matrix.values)
distances, indices = knn.kneighbors(matrix.values, n_neighbors=amount_of_recommendations)


index_for_movie = matrix.index.tolist().index(movie_to_select)    # get the index for movie 1
sim_movies = indices[index_for_movie].tolist()                    # find the indices for the similar movies
movie_distances = distances[index_for_movie].tolist()   # distances between movie 1 and the similar movies
id_movie = sim_movies.index(index_for_movie)            # the position of movie 1 in the list sim_movies
sim_movies.remove(index_for_movie)                      # remove movie 1 from the list sim_movies
movie_distances.pop(id_movie)                           # remove movie 1 from the list movie_distances
movie_similarity = np.array(movie_distances)            # omtoveren naar array om berekening op uit te voeren
movie_similarity = (1-movie_similarity)*100             # make inversion of distance: similarity of movies


print('The Nearest Movies to movie_1:', sim_movies)
print('The Distance from movie_1:', movie_distances)

#nieuw dataframe maken dat de films samenvoegt
movies_to_recommend = pd.DataFrame({'sim movies': sim_movies, 'movie similarity': movie_similarity})
similar = movies[movies.index.isin(movies_to_recommend['sim movies'])][['movieId', 'title']]       #hij stopt ze op verkeerde volgorde.
similar = pd.concat([movies, movies_to_recommend], axis=1).reindex(movies_to_recommend.index)[['title', 'sim movies', 'movie similarity']]

#print een voor een de films die het meest lijken op het nummer dat de gebruiker heeft ingevoerd
print()
print(f'The Nearest Movies to {movie_to_select} :\n')

for count in similar.index:
    a= similar[similar.index == count]
    print(a['title'].to_string(index=False))



