# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 10:39:18 2023
@author: silas

Dit is een script waarmee een nieuwe gebruiker ratings voor een film kan toevoegen. 
Dit kan daarna gebruikt worden om andere films aangeraden te krijgen.
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

#Een kleinere dataset maken en deze in een pivot table zetten
rating_klein = rating[rating['movieId']<=200]
matrix = rating_klein.pivot_table(values='rating', index='movieId', columns='userId', fill_value=0)


#nieuwe matrix aanmaken zodat je de oude niet verpest. 
matrix1 = matrix.copy()
matrix1.insert(0, 'user', 0)                                        #voeg een nieuwe gebruiker aan het begin toe

#film zoeken
film_input = input("Search a movie \n")
search_result = movies[movies['title'].str.contains(film_input, regex=False, case=False)]
print(search_result[['movieId', 'title', 'year']])
movieId_input = int(input('What movie Id did you mean? \n'))
rating_input = float(input('How would you rate this movie? \n'))

#voeg de inputs van de gebruiker in in het dataframe. Hij moet wel binnen de gekozen waarde vallen.
if movieId_input <= matrix.index.max():    
    matrix1.at[movieId_input,'user']=rating_input
else:
    print('This movie is not in the list, please try another movie')                       

