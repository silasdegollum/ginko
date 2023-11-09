#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:52:43 2023

@author: nivinebenjamin
"""
import seaborn as sns 
import sklearn as sk
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split

df = pd.read_csv('u.item')
df.head(30)

#datacleaning 

df = df[['title','year','genres']]
df = df.dropna()
df.head()
df['genres'].value_counts()

dummies = pd.get_dummies(df['genres'])
df = pd.concat([df,dummies], axis=0)
df.head()

x = df[['title','year']] # X matrix 

y = df['genres']
x_train, X_test, y_train, y_test = train_test_split(x, y,  test_size=0.3, random_state=1)
x_train.head()

from sklearn.neigbors import KNeighborsClassifier 

knn = KNeighborsClaaaifier()
knn = knn.fit(X_train, y_train)

