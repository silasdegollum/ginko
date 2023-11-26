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
tags = pd.read_csv(f'{folder_path}/tags.csv')

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

#opschonen dataset tags
tags = tags.drop(['userId', 'timestamp'], axis=1)
print(tags)
# Groepeer op 'movieId' en consolideer de tags in één kolom
consolidated_tags = tags.groupby('movieId')['tag'].agg(lambda x: ', '.join(x.dropna()) 
                                                       if x.notna().any() else None).reset_index()

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
num_rating = rating2.groupby('movieId')['rating'].count().rename('num_ratings')

# Koppel de dataframes op basis van de 'FilmID'-kolom
samengevoegd_df = pd.merge(movies2, avg_rating, on='movieId')
print(samengevoegd_df)

# Koppel de datasets op basis van meerdere kolommen
samengevoegd_df2 = pd.merge(samengevoegd_df, movies_cleaned, on=['movieId', 'title', 'year'], how='left')
samengevoegd_df3 = pd.merge(samengevoegd_df2, num_rating, on='movieId', how='left')
samengevoegd_df4 = pd.merge(samengevoegd_df3, consolidated_tags, on='movieId', how= 'left')
samengevoegd_df['year'] = samengevoegd_df["year"].dropna().astype(int)    

#nieuw dataframe maken voor tags en movieId
tags_overzicht = samengevoegd_df4[['title', 'tag']]

# Functie om specifieke tags te zoeken en weer te geven
def zoek_op_tags(tags_overzicht, zoekwoorden):
    # Controleer op NaN-waarden in de 'tag'-kolom
    geen_nan_waarden = tags_overzicht['tag'].notna()

    # Filter het DataFrame op basis van de zoekwoorden en zonder NaN-waarden
    gefilterd_df = tags_overzicht[geen_nan_waarden]

    # Voeg zoekcondities toe voor elk zoekwoord
    for zoekwoord in zoekwoorden:
        gefilterd_df = gefilterd_df[gefilterd_df['tag'].str.contains(zoekwoord, case=False, na=False)]

    # Toon het gefilterde DataFrame
    st.subheader(f"Resultaten voor '{', '.join(zoekwoorden)}':")
    st.write(gefilterd_df)

#bouwen in streamlit
import streamlit as st 

def main():
    st.title("Zoek een film")
    text = """
    LET OP! DE WEBSITE MAAKT GEBRUIK VAN EEN GROOT DATABESTAND WAARDOOR HET
    LADEN SOMS WAT LANGER DUURT!
    
    Hier kunt u opzoek gaan naar een specifieke film. 
    Voer hieronder de naam van de specifieke filmtitel in. 
    Hierna komen de films naar voren die passen bij de ingevoerde zoekwoorden.
    Hoe specifieker de titel is vermeld, hoe beter het zoekresultaat zal zijn.
    """
    st.write(text)
    
    # Invoerveld om de filmnaam in te voeren
    movie_title = st.text_input("Voer de titel van de film in:")
    
    if not movie_title:
        st.warning("Voer een filmtitel in om het gewenste resultaat te krijgen.")
    else:
  # Als er een filmnaam is ingevoerd, haal de informatie op
      df_cleaned = samengevoegd_df4.dropna()
      selected_movie = df_cleaned[df_cleaned["title"].str.contains(movie_title, regex=False, case=False)]
        
       # Controleer of de film is gevonden
    if not selected_movie.empty:
       # Toon filminformatie
       st.subheader("Gevonden films:")
       st.dataframe(selected_movie)
       #st.subheader(selected_movie["title"].iloc[0])
       #st.write("Jaar:", selected_movie["year"].iloc[0])
       #st.write("Rating:", selected_movie["rating"].iloc[0])
       
       # Combineer genres met komma's en toon
       #genres_str = ", ".join(selected_movie["genres"].iloc[0])
       #st.write("Genre:", genres_str)
    else:
       st.warning("Film niet gevonden. Probeer een andere titel.")

if __name__ == "__main__":
    main()  

def filter_movies(selected_genres, year_range):
    return movies[(movies['genres'].apply(lambda
                                          x: any(genre in x for genre 
                                        in selected_genres))) & (movies['year'] >= year_range[0]) 
                  & (movies['year'] <= year_range[1])]


#nieuwe hoofdtitel voor een pagina met een filter voor de verschillende ratings die zijn gedaan per film
def main():
    st.title("Filtering van films op basis van gegeven filters")
    text = """
    Op deze pagina kunt opzoek gaan naar films. Dit kan je doen door te filteren op jaartal, 
    genres, gemiddelde rating cijfer en het aantal gegeven ratings.
    Succes bij het zoeken naar een passende film op basis van je eigen gegeven imput.
    """
    st.write(text)
if __name__ == "__main__":
    main()

#INRICHTEN VAN DE SIDEBAR 
def main():
# Sidebar filter opties
    if st.sidebar.title ('Filter hier'):  
        year_range = st.sidebar.slider("Selecteer een jaartal:", 1874, 2019, (1874, 2019))
        genre_options = ["Adventure", "Animation", "Children", "Comedy", "Fantasy", "Romance", "Drama", 
                         "Action", "Crime", "Thriller", "Horror", "Mystery", "Sci-Fi", "IMAX",
                         "Documentary", "War", "Musical", "Western", "Film-Noir"]
        genre_search = st.sidebar.multiselect("Selecteer uw favoriete filmgenres:", genre_options,
                                              default=genre_options)
        selected_rate_s = st.sidebar.slider("Selecteer uw gewenste rating:", 0.0, 5.0, (0.0, 5.0))
        selected_num_min = st.sidebar.number_input("Voer het laagste aantal ratings in:", min_value=1,
                                                   max_value=81491, value=1)
        selected_num_max = st.sidebar.number_input("Voer het hoogste aantal ratings in:", min_value=1,
                                                   max_value=81491, value=81491)
       # selected_num = st.sidebar.slider("Selecteer uw gewenste aantal ratings", 1, 81491, (2, 80000))

# Sidebar invoervelden weergeven
    st.write(f"Uw gewenste jaartal is tussen:{year_range}")
    st.write(f"Uw gewenste genre is:{genre_search}")
    st.write(f"Uw geselecteerde rating is tussen: {selected_rate_s}")
    st.write(f"Uw gewenste aantal ratings is: tussen {selected_num_min} en {selected_num_max}")
    #st.write(f"Uw gewenste aantal ratings is: {selected_num}")

# Zorg ervoor dat de kolom 'year' wordt omgezet naar numerieke waarden
# Resultaten filteren op basis van alle geselecteerde criteria
    search_result2 = samengevoegd_df2[
        (pd.to_numeric(samengevoegd_df4['year'], errors='coerce') > year_range[0]) &
        (pd.to_numeric(samengevoegd_df4['year'], errors='coerce') < year_range[1]) &
        (pd.to_numeric(samengevoegd_df4['rating'], errors='coerce') > selected_rate_s[0]) &
        (pd.to_numeric(samengevoegd_df4['rating'], errors='coerce') < selected_rate_s[1]) &
        (samengevoegd_df4['genres'].apply(lambda x: isinstance(x, list) and any(item in genre_search
                                                                                for item in x))) &
        (pd.to_numeric(samengevoegd_df4['num_ratings'], errors='coerce') > selected_num_min) &
        (pd.to_numeric(samengevoegd_df4['num_ratings'], errors='coerce') < selected_num_max)
    ]
    
# Zorg ervoor dat de kolom 'year' wordt omgezet naar numerieke waarden
    condition_year = (pd.to_numeric(samengevoegd_df4['year'], errors='coerce') > year_range[0]) & (pd.to_numeric(samengevoegd_df4['year'], errors='coerce') < year_range[1])
    
# Voeg de genre-filtering alleen toe als genres zijn geselecteerd
    if genre_search:
        condition_genre = samengevoegd_df4['genres'].apply(lambda x: isinstance(x, list) and 
                                                           any(item in genre_search for item in x))
    else:
        # Als geen genres zijn geselecteerd, altijd waar
        condition_genre = True

    condition_rating = (pd.to_numeric(samengevoegd_df4['rating'], errors='coerce') > selected_rate_s[0]) & (pd.to_numeric(samengevoegd_df4['rating'], errors='coerce') < selected_rate_s[1])
    condition_num_ratings = (samengevoegd_df4['num_ratings'] >= selected_num_min) & (samengevoegd_df4
                                                            ['num_ratings'] <= selected_num_max)
    
    search_result2 = samengevoegd_df4[condition_year & condition_genre & condition_rating &
                                      condition_num_ratings]
    st.subheader('Gefilterde data')
    st.dataframe(search_result2)
    
if __name__ == "__main__":
    main()

if st.checkbox ('Toon het gehele ongefilterde databestand'):
    st.dataframe(samengevoegd_df4)

#bouwen nieuwe pagina voor zoeken op specifieke tags
#def main():
    st.title("Zoek op specifieke tags")
    text = """
    Op deze pagina kan je opzoek gaan naar films op basis van specifieke tags
    die zijn gegeven door de gebruikers. Denk hierbij aan een specifieke acteur.
    Klik op de regel waarin de tags staan, om alle tags die aan de film zitten te zien.
    """
    st.write(text)

    # Voeg een zoekfunctie toe
   # zoekwoord = st.text_input("Zoek op tags (gescheiden door komma)", "")
    
    #controleer op NaN-waarden in de tag's kolom
#    geen_nan_waarden = tags_overzicht['tag'].notna()

    # Filter het DataFrame op basis van het zoekwoord
   # gefilterd_df = tags_overzicht[geen_nan_waarden & tags_overzicht['tag'].str.contains(zoekwoord, case=False, na=False)]
    
    # Toon het gefilterde DataFrame als zoekwoord is ingevoerd
   # if zoekwoord:
       # st.subheader(f"Resultaten voor '{zoekwoord}':")
       # st.write(gefilterd_df)

   # Toon de resultaten
  #  st.write("Gefilterde resultaten:")
   # st.write(tags_overzicht)
#if __name__ == "__main__":
    main()

# Functie om specifieke tags te zoeken en weer te geven
def zoek_op_tags(tags_overzicht, zoekwoorden):
    # Controleer op NaN-waarden in de 'tag'-kolom
    geen_nan_waarden = tags_overzicht['tag'].notna()

    # Filter het DataFrame op basis van de zoekwoorden en zonder NaN-waarden
    gefilterd_df = tags_overzicht[geen_nan_waarden & tags_overzicht['tag'].str.contains('|'.join(zoekwoorden), case=False, na=False)]

    for zoekwoord in zoekwoorden:
        gefilterd_df = gefilterd_df[gefilterd_df['tag'].str.contains(zoekwoord, case=False, na=False)]
    # Toon het gefilterde DataFrame
    st.subheader(f"Resultaten voor '{', '.join(zoekwoorden)}':")
    st.write(gefilterd_df)

# Streamlit-applicatie
def main():
    st.title("Zoek op specifieke tags")
    text = """
    Op deze pagina kan je opzoek gaan naar films op basis van specifieke tags
    die zijn gegeven door de gebruikers. Denk hierbij aan een specifieke acteur.
    Klik op de regel waarin de tags staan, om alle tags die aan de film zitten te zien.
    """
    st.write(text)

    # Voeg een zoekfunctie toe
    zoekwoord = st.text_input("Zoek op tags", "")

    # Voeg een knop toe om het zoekwoord toe te voegen aan de lijst
    if st.button("Voeg toe aan zoeklijst", key="add_button"):
        zoekwoorden = zoekwoord.split(',')
        zoekwoorden = [woord.strip() for woord in zoekwoorden if woord.strip()]  # Verwijder lege strings
        st.session_state.zoekwoordenlijst.extend(zoekwoorden)

    # Voeg een knop toe om alle zoekwoorden te verwijderen
    if st.button("Verwijder alle zoekwoorden", key="clear_button"):
        st.session_state.zoekwoordenlijst = []

    # Toon de huidige zoekwoordenlijst
        st.subheader("Huidige zoekwoordenlijst:")
        st.write(st.session_state.zoekwoordenlijst)
    
    #st.subheader("Tags overzicht")
    #st.write(tags_overzicht)

    # Voer de zoekfunctie uit op basis van de zoekwoordenlijst
    zoek_op_tags(tags_overzicht, st.session_state.zoekwoordenlijst)


if __name__ == "__main__":
    # Initialiseer de zoekwoordenlijst in de sessie
    if 'zoekwoordenlijst' not in st.session_state:
        st.session_state.zoekwoordenlijst = []

    main()



