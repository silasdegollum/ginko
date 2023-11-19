# -*- coding: utf-8 -*-
"""
Spyder Editor @marloesvanettikhoven

This is a temporary script file.
"""
import pandas as pd
#data opschonen
#openen van de map
folder_path = '/Users/MarloesvanEttikhoven/Desktop/dataset 25m'

#mappen individueel openen
genome_score = pd.read_csv(f'{folder_path}/genome-scores.csv')
genome_tags = pd.read_csv(f'{folder_path}/genome-tags.csv')
movies = pd.read_csv(f'{folder_path}/movies.csv')
ratings = pd.read_csv(f'{folder_path}/ratings.csv')
tags = pd.read_csv(f'{folder_path}/ratings.csv')

#movies dataframe verbeteren door jaartal in een losse kolom te zetten
movies[['title', 'year']] = movies['title'].str.extract(r'(.+) \((\d{4})\)')
print(movies)

#genres splitsen
movies['genres'] = movies['genres'].str.split('|')
print(movies)

# Verwijder rijen waarin de waarde in de kolom "title" None is
movies_cleaned = movies.dropna(subset=['title'])
# Toon het resultaat
print(movies_cleaned)

# Vraag de gebruiker om een genre in te voeren
#search_genre = input("Voer het genre in waarop je wilt zoeken: ")

# Zoek films met het opgegeven genre
#search_result = movies[movies['genres'].apply(lambda x: search_genre in x)]
#print(search_result)

#bouwen in streamlit (vanaf hier afspelen anders moet je telkens genre invullen)
import streamlit as st 

def filter_movies(selected_genres, year_range):
    return movies[(movies['genres'].apply(lambda x: any(genre in x for genre in selected_genres))) & (movies['year'] >= year_range[0]) & (movies['year'] <= year_range[1])]

def main():
    st.title("Filtering films MovieLens")
    text = """
    Hier kunt op opzoek gaan naar de films per genre en jaartal. Op basis van het gekozen genre krijgt u de gehele lijst te zien met films die in dit genre passen. 
    Verder kunt u ook zoeken op basis van het jaartal van de films. De films komen uit de jaren 1874 tm 2019
    """
    st.write(text)
    # Stel een vraag over het genre van films
    genre_options = ["Adventure", "Animation", "Children", "Comedy", "Fantasy", "Romance", "Drama", "Action", "Crime", "Thriller", "Horror", "Mystery", "Sci-Fi", "IMAX", "Documentary", "War", "Musical", "Western", "Film-Noir"]
    selected_genre = st.selectbox("Selecteer uw favoriete filmgenre:", genre_options)
    
    # Toon de geselecteerde genre
    st.write(f"Uw geselecteerde genre is: {selected_genre}")
    search_result = movies_cleaned[movies_cleaned['genres'].apply(lambda x: selected_genre in x)]
   
    st.subheader (f"{selected_genre}")
    st.dataframe(search_result)
if __name__ == "__main__":
    main()

if st.checkbox ('show raw data'):
    st.subheader ('raw data')
    st.dataframe(movies_cleaned)

# Sidebar met filters
if st.sidebar.title ('Filter hier'): 
    year_range = st.sidebar.slider("Selecteer een jaartal:", 1874, 2019, (1874, 2019))
    genre_options = ["Adventure", "Animation", "Children", "Comedy", "Fantasy", "Romance", "Drama", "Action", "Crime", "Thriller", "Horror", "Mystery", "Sci-Fi", "IMAX", "Documentary", "War", "Musical", "Western", "Film-Noir"]
    genre_search = st.sidebar.multiselect("Selecteer uw favoriete filmgenres:", genre_options, default=genre_options)

#nieuwe pagina met een filter voor de verschillende ratings die zijn gedaan per film
def main():
    st.title("Filtering op basis van de film rates")
    text = """
    Op deze pagina kunt opzoek gaan naar films en hun desbetreffende ratings.
    Deze ratings zijn gedaan door de gebruikers van de website movielens. De cijfers varieren van 0 tot en met 5. 
    """
    st.write(text)
    
    # Stel een vraag over de rating van de film
    rating_options = ["0.5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"]
    selected_rating = st.selectbox("Selecteer uw rating voorkeur:", rating_options)
   
    #Toon geselecteerde rating
    st.write(f"Uw geselecteerde rating is: {selected_rating}")
    
    #pas filter aan
    selected_rating = float(selected_rating)
    search_result1 = ratings[ratings['rating'] == selected_rating]
   
    st.subheader (f"Films met rating {selected_rating}")
    st.dataframe(search_result1)
 
if __name__ == "__main__":
    main()
    
    
    