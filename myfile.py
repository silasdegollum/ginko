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

#filmdata inladen en de genres elk in een eigen kolom zetten. (Sillas)
movies2 = pd.read_csv(r"/Users/MarloesvanEttikhoven/Desktop/Dataset 25m/movies.csv")
genres = movies2['genres'].str.split('|', expand=True)           #Deze split de genres in hun eigen deel
dummies = pd.get_dummies(genres[0])                         #Deze tovert het weer om in alle genres en binair of een film ze bezit
del movies2['genres']
movies2_ = pd.concat([movies2, dummies], axis=1)                       #Dit voegt de kolommen bij de eerste dataset
movies2_correct = movies2.set_index('movieId')

#movies dataframe verbeteren door jaartal in een losse kolom te zetten
movies2[['title', 'year']] = movies2['title'].str.extract(r'(.+) \((\d{4})\)')

#rating data inladen (Sillas)
rating2 = pd.read_csv(r"/Users/MarloesvanEttikhoven/Desktop/Dataset 25m/ratings.csv").astype(float)

#gemiddelde rating berekenen (Sillas)
avg_rating = rating2.groupby('movieId')['rating'].mean()
avg_rating.index = avg_rating.index.astype(int)
num_rating = rating2.groupby('movieId')['rating'].count()

# Koppel de dataframes op basis van de 'FilmID'-kolom
samengevoegd_df = pd.merge(movies2, avg_rating, on='movieId')
print(samengevoegd_df)

# Koppel de datasets op basis van meerdere kolommen
samengevoegd_df2 = pd.merge(samengevoegd_df, movies_cleaned, on=['movieId', 'title', 'year'], how='left')
samengevoegd_df['year'] = samengevoegd_df["year"].dropna().astype(int)    


#bouwen in streamlit
import streamlit as st 

def main():
    st.title("Zoek een film")
    text = """
    Hier kunt u opzoek gaan naar een specifieke film. 
    Voer hieronder de naam van de specifieke filmtitel in. 
    Belangrijk is dat de filmtitel precies wordt overgenomen. Denk hierbij aan hoofdletters, komma's, uitroeptekens en vraagtekens.'
    De website is hiervoor erg gevoelig.
    """
    st.write(text)
    
    # Invoerveld om de filmnaam in te voeren
    movie_title = st.text_input("Voer de titel van de film in:")
    
    if movie_title:
    # Als er een filmnaam is ingevoerd, haal de informatie op
        selected_movie = samengevoegd_df2[samengevoegd_df2["title"] == movie_title]

       # Controleer of de film is gevonden
    if not selected_movie.empty:
       # Toon filminformatie
       #st.subheader(selected_movie["title"].iloc[0]) (overleggen of deze functie moet ja of nee)
       st.write("Jaar:", selected_movie["year"].iloc[0])
       st.write("Rating:", selected_movie["rating"].iloc[0])
       
       # Combineer genres met komma's en toon
       genres_str = ", ".join(selected_movie["genres"].iloc[0])
       st.write("Genre:", genres_str)
    else:
       st.warning("Film niet gevonden. Probeer een andere titel.")

if __name__ == "__main__":
    main()  

def filter_movies(selected_genres, year_range):
    return movies[(movies['genres'].apply(lambda x: any(genre in x for genre in selected_genres))) & (movies['year'] >= year_range[0]) & (movies['year'] <= year_range[1])]


#nieuwe hoofdtitel voor een pagina met een filter voor de verschillende ratings die zijn gedaan per film
def main():
    st.title("Filtering van films op basis van gegeven filters")
    text = """
    Op deze pagina kunt opzoek gaan naar films. Dit kan je doen door te filteren op jaartal, genres en ratings.
    Succes bij het zoeken naar een passende film op basis van je eigen gegeven imput
    """
    st.write(text)
if __name__ == "__main__":
    main()

#INRICHTEN VAN DE SIDEBAR 
def main():
# Sidebar filter opties
    if st.sidebar.title ('Filter hier'):  
        year_range = st.sidebar.slider("Selecteer een jaartal:", 1874, 2019, (1874, 2019))
        genre_options = ["Adventure", "Animation", "Children", "Comedy", "Fantasy", "Romance", "Drama", "Action", "Crime", "Thriller", "Horror", "Mystery", "Sci-Fi", "IMAX", "Documentary", "War", "Musical", "Western", "Film-Noir"]
        genre_search = st.sidebar.multiselect("Selecteer uw favoriete filmgenres:", genre_options, default=genre_options)
        selected_rate_s = st.sidebar.slider("Selecteer uw gewenste rating:", 0.0, 5.0, (1.0, 4.0))

# Sidebar invoervelden weergeven
    st.write(f"Uw gewenste jaartal is:{year_range}")
    st.write(f"Uw gewenste genre is:{genre_search}")
    st.write(f"Uw geselecteerde rating is: {selected_rate_s}")

# Zorg ervoor dat de kolom 'year' wordt omgezet naar numerieke waarden
# Resultaten filteren op basis van alle geselecteerde criteria
    search_result2 = samengevoegd_df2[
        (pd.to_numeric(samengevoegd_df2['year'], errors='coerce') > year_range[0]) &
        (pd.to_numeric(samengevoegd_df2['year'], errors='coerce') < year_range[1]) &
        (pd.to_numeric(samengevoegd_df2['rating'], errors='coerce') > selected_rate_s[0]) &
        (pd.to_numeric(samengevoegd_df2['rating'], errors='coerce') < selected_rate_s[1]) &
        (samengevoegd_df2['genres'].apply(lambda x: isinstance(x, list) and any(item in genre_search for item in x)))
    ]
    
# Zorg ervoor dat de kolom 'year' wordt omgezet naar numerieke waarden
    condition_year = (pd.to_numeric(samengevoegd_df2['year'], errors='coerce') > year_range[0]) & (pd.to_numeric(samengevoegd_df2['year'], errors='coerce') < year_range[1])
# Voeg de genre-filtering alleen toe als genres zijn geselecteerd
    if genre_search:
        condition_genre = samengevoegd_df2['genres'].apply(lambda x: isinstance(x, list) and any(item in genre_search for item in x))
    else:
        # Als geen genres zijn geselecteerd, altijd waar
        condition_genre = True

    condition_rating = (pd.to_numeric(samengevoegd_df2['rating'], errors='coerce') > selected_rate_s[0]) & (pd.to_numeric(samengevoegd_df2['rating'], errors='coerce') < selected_rate_s[1])
    
    search_result2 = samengevoegd_df2[condition_year & condition_genre & condition_rating]
   
    st.subheader('Gefilterde data')
    st.dataframe(search_result2)
    
if __name__ == "__main__":
    main()

if st.checkbox ('show het gehele ongefilterde databestand'):
    st.dataframe(samengevoegd_df2)
