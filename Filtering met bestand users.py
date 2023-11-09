#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 11:15:20 2023

@author: MarloesvanEttikhoven
"""

import pandas as pd

#inladen van databestand
movies2 = pd.read_csv('/Users/MarloesvanEttikhoven/Desktop/users.csv')

#kolommen opsplitsen in meerdere kolommen
movies2[['UserID', 'Gender', 'Age', 'Occupation', 'Zipcode']] = movies2['UserID;Gender;Age;Occupation;ZipCode'].str.split(';', 5, expand=True)

#oorspronkelijke kolom verwijderen
movies2.drop(columns=['UserID;Gender;Age;Occupation;ZipCode'], inplace=True)

#toon nieuwe dataframe met alle nieuwe kolommen
print(movies2)

#verwijder de kolom ZipCode, want deze is niet relevant
movies2.drop(columns=['Zipcode'], inplace=True)

# Maak een lijst met unieke 'Occupation'-soorten
occupations = movies2['Occupation'].unique()

#nieuw dataframe met aantal gebruikers per occupation
occupation_counts = movies2.groupby('Occupation').size().reset_index(name='Aantal Gebruikers')

#nieuw dataframe met aantal gebruikers per age
age_counts = movies2.groupby('Age').size().reset_index(name='Aantal Gebruikers')

# Vraag gebruiker om leeftijd en geslacht in te voeren
gewenste_leeftijd = int(input("Voer de gewenste leeftijd in: "))
gewenst_geslacht = input("Voer het gewenste geslacht in (M/F): ")

# Filter de DataFrame op basis van de ingevoerde leeftijd en geslacht
gefilterde_films = movies2[(movies2['Age'] == str(gewenste_leeftijd)) & (movies2['Gender'] == gewenst_geslacht)]

# Toon de gefilterde DataFrame
print("\nGefilterde DataFrame:")
print(gefilterde_films)



 






