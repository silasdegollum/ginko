# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 19:07:45 2023
@author: silas

Dit is een code die films aanraadt voor een in te stellen gebruiker op basis van ratings. Dit is dus unsupervised learning.
Hij maakt geen gebruik van andere informatie over de films. 

"""

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

#filmdata inladen en de genres elk in een eigen kolom zetten.
movies = pd.read_csv(r"C:\Users\silas\Documents\HU\5Minor\Periode 2\Data\ml-25m\ml-25m\movies.csv")
genres = movies['genres'].str.split('|', expand=True)              #Deze split de genres in hun eigen deel
dummies = pd.get_dummies(genres[0])                                #Deze tovert het weer om in alle genres en binair of een film ze bezit
movies['genres'] = movies['genres'].str.split('|')
movies = pd.concat([movies, dummies], axis=1)                      #Dit voegt de kolommen bij de eerste dataset
movies[['title', 'year']] = movies['title'].str.extract(r'(.+) \((\d{4})\)')    #extraheert publicatiejaar uit de filmnaam
movies['year'] = movies['year'].dropna().astype(int)
movies = movies.set_index('movieId')

#rating data inladen
rating = pd.read_csv(r"C:\Users\silas\Documents\HU\5Minor\Periode 2\Data\ml-25m\ml-25m\ratings.csv").astype(float)
rating[['userId', 'movieId', 'timestamp']] = rating[['userId', 'movieId', 'timestamp']].astype(int)

#gemiddelde rating berekenen en bij de movie dataset gooien
avg_rating = rating.groupby('movieId')['rating'].mean()
avg_rating.index = avg_rating.index.astype(int)
num_ratings = rating.groupby('movieId')['rating'].count().rename('num_ratings')
movies = pd.concat([movies, avg_rating], axis=1) 
movies = pd.concat([movies, num_ratings], axis=1) 
movies = movies.reset_index()                                       #index moet weer gereset worden voor de lookuptabel
movies = movies.dropna()                                            #er is een heel aantal films zonder rating

#Een kleinere dataset maken en deze in een pivot table zetten
rating_klein = rating[rating['movieId']<=200]
matrix = rating_klein.pivot_table(values='rating', index='movieId', columns='userId', fill_value=0)


#voeg een nieuwe gebruiker aan het begin toe

matrix.insert(0, 1, 0)                                        

#film zoeken
def search():
    film_input = input("Search a movie \n")
    search_result = movies[movies['title'].str.contains(film_input, regex=False, case=False)]
    print(search_result[['movieId', 'title', 'year']])
    movieId_input = int(input('What movie Id did you mean? \n'))
    rating_input = float(input('How would you rate this movie? \n'))

    #voeg de inputs van de gebruiker in in het dataframe. Hij moet wel binnen de gekozen waarde vallen.
    if movieId_input <= matrix.index.max():    
        matrix.at[movieId_input,1]=rating_input
    else:
        print('This movie is not in the list, please try another movie')  

matrix = matrix.dropna()
   

"""
Hier begint de code voor het aanbevelen. Dit heb ik niet zelf geschreven, maar komt van deze website:
    https://towardsdatascience.com/item-based-collaborative-filtering-in-python-91f747200fab
    Ik heb er wel het een en adner in aangepast.
"""

def recommend():
    #variabelendefinitie
    number_neighbors = 6
    user_name = 1



    matrix1 = matrix.copy()

    #finding nearest neighbors
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(matrix1.values)
    distances, indices = knn.kneighbors(matrix1.values, n_neighbors=number_neighbors)

    # convert user_name to user_index
    user_index = matrix1.columns.tolist().index(user_name)


    # t: movie_title, m: the row number of t in df
    for m,t in list(enumerate(matrix.index)):
      
      # find movies without ratings by user_4
      if matrix.iloc[m, user_index] == 0:
        sim_movies = indices[m].tolist()
        movie_distances = distances[m].tolist()
        
        # Generally, this is the case: indices[3] = [3 6 7]. The movie itself is in the first place.
        # In this case, we take off 3 from the list. Then, indices[3] == [6 7] to have the nearest NEIGHBORS in the list. 
        if m in sim_movies:
          id_movie = sim_movies.index(m)
          sim_movies.remove(m)
          movie_distances.pop(id_movie) 

        # However, if the percentage of ratings in the dataset is very low, there are too many 0s in the dataset. 
        # Some movies have all 0 ratings and the movies with all 0s are considered the same movies by NearestNeighbors(). 
        # Then,even the movie itself cannot be included in the indices. 
        # For example, indices[3] = [2 4 7] is possible if movie_2, movie_3, movie_4, and movie_7 have all 0s for their ratings.
        # In that case, we take off the farthest movie in the list. Therefore, 7 is taken off from the list, then indices[3] == [2 4].
        else:
          sim_movies = sim_movies[:number_neighbors-1]
          movie_distances = movie_distances[:number_neighbors-1]
            
        # movie_similarty = 1 - movie_distance    
        movie_similarity = [1-x for x in movie_distances]
        movie_similarity_copy = movie_similarity.copy()
        nominator = 0

        # for each similar movie
        for s in range(0, len(movie_similarity)):
          
          # check if the rating of a similar movie is zero
          if matrix.iloc[sim_movies[s], user_index] == 0:

            # if the rating is zero, ignore the rating and the similarity in calculating the predicted rating
            if len(movie_similarity_copy) == (number_neighbors - 1):
              movie_similarity_copy.pop(s)
              
            else:
              movie_similarity_copy.pop(s-(len(movie_similarity)-len(movie_similarity_copy)))

          # if the rating is not zero, use the rating and similarity in the calculation
          else:
            nominator = nominator + movie_similarity[s]*matrix.iloc[sim_movies[s],user_index]

        # check if the number of the ratings with non-zero is positive
        if len(movie_similarity_copy) > 0:
          
          # check if the sum of the ratings of the similar movies is positive.
          if sum(movie_similarity_copy) > 0:
            predicted_r = nominator/sum(movie_similarity_copy)

          # Even if there are some movies for which the ratings are positive, some movies have zero similarity even though they are selected as similar movies.
          # in this case, the predicted rating becomes zero as well  
          else:
            predicted_r = 0

        # if all the ratings of the similar movies are zero, then predicted rating should be zero
        else:
          predicted_r = 0

      # place the predicted rating into the copy of the original dataset
        matrix1.iloc[m,user_index] = predicted_r



    #Ik dit onderdeel uit de functie gehaald omdat je dan wel te zien krijgt wat variabalen zijn
    print(f'The list of the Movies user {user_name} Has Watched \n')                

    for m in matrix[matrix[user_name] > 0][user_name].index.tolist():
        m_titel = movies[movies['movieId']==m]['title'].to_string(index=False)      #om niet alleen een ID maar ook filmnaam weer te geven
        print(m_titel)
      
    print('\n')

    recommended_movies = []

    for m in matrix[matrix[user_name] == 0].index.tolist():                         #hier voeg je iteratief alle eigenschappen van de film toe
        m_titel = movies[movies['movieId']==m]['title'].to_string(index=False)      
        m_jaartal = movies[movies['movieId']==m]['year'].to_string(index=False)
        m_avg_rating = movies[movies['movieId']==m]['rating'].to_string(index=False)
        m_num_ratings = movies[movies['movieId']==m]['num_ratings'].to_string(index=False)
        m_genres = movies[movies['movieId']==m]['genres'].to_string(index=False)        #geeft nog steeds als een list weer, niet zo mooi.
        index_matrix = matrix.index.tolist().index(m)
        predicted_rating = matrix1.iloc[index_matrix, matrix1.columns.tolist().index(user_name)]
        recommended_movies.append((m_titel, m_jaartal, predicted_rating, m_avg_rating, m_num_ratings, m_genres))  #stop ze in een lijst

    sorted_rm = sorted(recommended_movies, key=lambda x:x[2], reverse=True)         #deze sorteert bovengenoemde lijst op predicted rating (derde nummer in tuple)
      
    print('The list of the Recommended Movies \n')
    rank = 1
    for recommended_movie in sorted_rm[:number_neighbors]:                      #print voor het aantal aanbevolen films de informatie
        
        print(f' {rank}: {recommended_movie[0]} \n '
              f'year: {recommended_movie[1]} \n'
              f' predicted rating: {recommended_movie[2]} \n'
              f' average rating: {recommended_movie[3]} \n'
              f' number of ratings: {recommended_movie[4]} \n'
              f' genres: {recommended_movie[5]}')
        print('\n')
        rank = rank + 1





