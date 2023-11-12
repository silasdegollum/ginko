#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues Nov  7 14:12:04 2023

@author: nivinebenjamin
recommendation system based on ratings 
"""

import pandas as pd
import numpy as np 

#make dataframe 1: user info 
columns_name = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv("/Users/nivinebenjamin/Desktop/Jaar 4/minor/blok 2/u.data", sep="\t", names=
columns_name)

print (df.head())
df.shape 

# maak dataframe 2: film info 
movies= pd.read_csv("/Users/nivinebenjamin/Desktop/Jaar 4/minor/blok 2/movies.csv", 
header= None)

print(movies.shape)
movies.head()

movies=movies[[0,1]]
movies.head()

movies.columns=["item.id","title"]

#samen voegen van de dataframes 
df=pd.merge(df,movies, left_on="item_id", right_on="item.id")

df.groupby("title").mean()['rating'].sort_values(ascending=False)

#nieuw dataframe average rating and number of rating for every movie 
ratings=pd.DataFrame(df.groupby('title').mean()['rating'])
ratings['number of ratings']=pd.DataFrame(df.groupby('title').count()['rating'])
print(ratings.head())

ratings.sort_values(by='rating', ascending=False)

#dataviz
import matplotlib.pyplot as plt 
import seaborn as sns 
sns.set_style("dark")

#histogram of the number of ratings 
plt.figure(figsize=(12,8))
plt.hist(ratings['number of ratings'], bins=70)
plt.show 

#histogram average rating
plt.hist(ratings['rating'],bins=70)
plt.show 

sns.jointplot(x='rating', y='number of ratings', data=ratings, alpha=0.5)


#recommendation system met referentie naar een specifieke film 
moviematrix=df.pivot_table(index="user_id", columns="title", values="rating")
print(moviematrix)


#info over film Star Wars 
starwars_user_ratings=moviematrix['Star Wars (1977)']
starwars_user_ratings.head()

# vinden correlatie star wars film met de andere films 
similar_to_starwas=moviematrix.corrwith(starwars_user_ratings)
similar_to_starwars

corr_starwars=pd.DataFrame(similar_to_starwas, columns=['correlation'])
corr_starwars.head()

corr_starwars.dropna(inplace=True)

corr-starwars.sort_values('correlation', ascending=False).head(10)

corr_starwars=corr-starwars.join(ratings['number of ratings'])
corr_starwars.head()

corr_starwars[corr_starwars['number of ratings']>100].sort_values('correlation',ascending=False)


#Recommendation functie 
def predict_movies(movie_name):
    movie_user_ratings=moviematrix[movie_name]
    similar_to_movie=moviematrix.corrwith(movie_user_ratings)
    corr_movie=pd.DataFrame(similar_to_movie,columns=['correlation'])
    
    corr_movie.dropna(inplace=True)
    corr_movie=corr_movie.join(ratings['number of ratings'])
    predictions=corr_movie[corr_movie['number of ratings']>100].sort_values('correlation', ascending=False)
    return predictions
predictions =predict-movies("As Good As It Gets (1997)")
#elke film kan gekozen worden
predictions.head()






