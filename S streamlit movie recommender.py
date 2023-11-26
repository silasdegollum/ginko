# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:38:41 2023
@author: silas

Dit script maakt een website in streamlit die films aan kan raden op basis van trainingsdata die op de website zelf wordt opgebouwd

"""

import pandas as pd
import streamlit as st

st.button("Rerun")

@st.cache_data
def load():
    movies = pd.read_csv(r"C:\Users\silas\Documents\GitHub\ginko\movies_bewerkt").set_index('movieId')
    del movies['Unnamed: 0']
    movies.insert(0, 'user', 0)
    return movies

movies = load()
movies_copy = movies.copy()

"""
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
"""


def inpu():
    st.title('Welcome, new user')
    film_input = st.text_input('Search a movie')
    st.write('movies containing that word:')
    search_result = movies[movies['title'].str.contains(film_input, regex=False, case=False)]
    st.dataframe(search_result)
    movieId_input = st.slider('movieId',0,2000)
    rating_input = st.slider('rating',0,5)


    if st.button('add this rating'):
        movies.at[movieId_input,'user']=rating_input
    return movies

movies = inpu()
st.dataframe(movies)

#if movieId_input <= movies.index.max():
 #    movies.at[movieId_input,'user']=rating_input
#else:
 #   st.write('This movie is not in the list, please try another movie')
