#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:27:00 2023

@author: MarloesvanEttikhoven
"""
import pandas as pd

#lezen van het csv bestand
movies = pd.read_csv('/Users/MarloesvanEttikhoven/Desktop/movielens_100k.csv')

#Aantal films uit het een bepaald jaar 
gewenst_jaar = 1995
gefilterde_df = movies[movies['year'] == gewenst_jaar]

#proberen
movies.sort_values("year")

movies[["genres", "year"]]

movies[movies["year"] < 1990]

#subsetting based on text data
genre_kolom = "genres"
gewenste_genres = ["comedy", "drama"]

genres_df = movies[movies["genres"] == gewenste_genres]


#nieuwe test
# Vervang "jaar_kolom" door de daadwerkelijke naam van de kolom met het jaartal
# Vervang "genre_kolom" door de daadwerkelijke naam van de kolom met het genre
gewenst_jaar = 1995  # Vervang dit door het gewenste jaar
gewenste_genres = ["Comedy", "Drama"]  # Vervang dit door de gewenste genres

# Filter de DataFrame op basis van het gewenste jaar en genres
nieuwe_df = movies[(movies['year'] == gewenst_jaar) & (movies['genres'].isin(gewenste_genres))]

# Toon de gefilterde DataFrame
print(nieuwe_df)


