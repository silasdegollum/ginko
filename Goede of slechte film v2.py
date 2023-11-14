# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 11:16:28 2023

@author: silas
"""


import seaborn as sns
import sklearn as sk
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

#filmdata inladen en de genres elk in een eigen kolom zetten.
movies = pd.read_csv(r"C:\Users\silas\Documents\HU\5Minor\Periode 2\Data\ml-25m\ml-25m\movies.csv")
genres = movies['genres'].str.split('|', expand=True)           #Deze split de genres in hun eigen deel
dummies = pd.get_dummies(genres[0])                         #Deze tovert het weer om in alle genres en binair of een film ze bezit
del movies['genres']
movies = pd.concat([movies, dummies], axis=1)                       #Dit voegt de kolommen bij de eerste dataset
movies = movies.set_index('movieId')


#rating data inladen
rating = pd.read_csv(r"C:\Users\silas\Documents\HU\5Minor\Periode 2\Data\ml-25m\ml-25m\ratings.csv").astype(float)

#gemiddelde rating berekenen
avg_rating = rating.groupby('movieId')['rating'].mean()
avg_rating.index = avg_rating.index.astype(int)

#dataframes even groot maken, is nodig voor het model zometeen. Ze worden ook gelijk gecombineerd in een df dat result heet.
result = pd.concat([movies, avg_rating], axis=1).reindex(avg_rating.index)

#Hier stel ik twee variabelen in voor de gebruiker.
aantal_buren = 2
minimale_score = 3

result['good movie'] = result['rating']>minimale_score #dit is de variabele die ik uiteindelijk in mijn model ga toetsen, als een film beter dan 3 scoort is hij goed.

X = result[['(no genres listed)', 'Action', 'Adventure',
       'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
       'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery',
       'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']]
y = result['good movie'].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

#Nu gaat hij het model trainen.
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
knn = KNeighborsClassifier(n_neighbors=aantal_buren)
knn = knn.fit(X_train, y_train)

#En print de uiteindelijke score
y_test_pred = knn.predict(X_test.values)
cm = confusion_matrix(y_test, y_test_pred)
report = classification_report(y_test, y_test_pred)
score = knn.score(X_test.values, y_test.values)
print(cm)
print(report)
print(score)


#Hier probeer ik te achterhalen wat de score van een nieuwe film wordt, maar weet niet wat true en false is. 
nieuwefilm = [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
print(knn.predict_proba([nieuwefilm]))



















