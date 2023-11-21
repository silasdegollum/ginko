# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:34:21 2023

@author: silas
"""

import pandas as pd


movies = pd.read_csv(r"C:\Users\silas\Documents\HU\5Minor\Periode 2\Data\ml-25m\ml-25m\movies.csv")
genres = movies['genres'].str.split('|', expand=True)              #Deze split de genres in hun eigen deel
dummies = pd.get_dummies(genres[0])                                #Deze tovert het weer om in alle genres en binair of een film ze bezit
movies['genres'] = movies['genres'].str.split('|')
movies = pd.concat([movies, dummies], axis=1)                      #Dit voegt de kolommen bij de eerste dataset
movies[['title', 'year']] = movies['title'].str.extract(r'(.+) \((\d{4})\)')    #extraheert publicatiejaar uit de filmnaam
movies['year'] = movies['year'].dropna().astype(int)
movies = movies.set_index('movieId')


#gemiddelde rating berekenen en bij de movie dataset gooien

movies = movies.reset_index()                                       #index moet weer gereset worden voor de lookuptabel
movies = movies.dropna()        


tags = pd.read_csv(r"C:\Users\silas\Documents\HU\5Minor\Periode 2\Data\ml-25m\ml-25m\tags.csv").dropna()[['movieId', 'tag']]

film_input = input("zoek een tag \n")
search_result = tags[tags['tag'].str.contains(film_input, regex=False, case=False)]

search_group = search_result.groupby('movieId')['tag'].count()
print(search_group['tag']>0)
