# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:40:33 2023

@author: silas
"""


import pandas as pd
import numpy as np

#filmdata inladen en de genres elk in een eigen kolom zetten.
movies = pd.read_csv(r"C:\Users\silas\Documents\HU\5Minor\Periode 2\Data\ml-25m\ml-25m\movies.csv")
genres = movies['genres'].str.split('|', expand=True)              #Deze split de genres in hun eigen deel
dummies = pd.get_dummies(genres[0])                                #Deze tovert het weer om in alle genres en binair of een film ze bezit
movies['genres'] = movies['genres'].str.split('|')
movies = pd.concat([movies, dummies], axis=1)                      #Dit voegt de kolommen bij de eerste dataset
movies[['title', 'year']] = movies['title'].str.extract(r'(.+) \((\d{4})\)')    #extraheert publicatiejaar uit de filmnaam
movies['year'] = movies['year'].dropna().astype(int)
movies = movies.set_index('movieId')

#rating data inladen
rating = pd.read_csv(r"C:\Users\silas\Documents\HU\5Minor\Periode 2\Data\ml-25m\ml-25m\ratings.csv").astype(float)
rating[['userId', 'movieId', 'timestamp']] = rating[['userId', 'movieId', 'timestamp']].astype(int)

#gemiddelde rating berekenen en bij de movie dataset gooien
avg_rating = rating.groupby('movieId')['rating'].mean()
avg_rating.index = avg_rating.index.astype(int)
num_ratings = rating.groupby('movieId')['rating'].count().rename('num_ratings')
movies = pd.concat([movies, avg_rating], axis=1) 
movies = pd.concat([movies, num_ratings], axis=1) 
movies = movies.reset_index()                                       #index moet weer gereset worden voor de lookuptabel
movies = movies.dropna()                                            #er is een heel aantal films zonder rating
movies.to_csv("movies_bewerkt")

#Een kleinere dataset maken en deze in een pivot table zetten
rating_klein = rating[rating['userId']<=2000]
matrix = rating_klein.pivot_table(values='rating', index='movieId', columns='userId', fill_value=0)
matrix.to_csv('matrix')
