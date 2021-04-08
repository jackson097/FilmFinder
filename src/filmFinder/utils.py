import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from Movies.models import Movie, MovieGenre, MoviePerson
from Genres.models import Genre
from Person.models import Person

def get_data():
    movies = Movie.objects.all()
    movies_genres = MovieGenre.objects.all()
    movies_people = MoviePerson.objects.all()
    people = Person.objects.all()
    all_genres = Genre.objects.all()

    data = []

    for movie in movies:
        movie_id = movie.movie_id
        title = movie.title
        genres = ""
        cast = ""
        plot = movie.overview

        # Create list of genres
        movie_genre = movies_genres.filter(movie_id=movie.movie_id)

        for genre in movie_genre:
            genres += all_genres.get(genre_id=genre.genre_id.genre_id).genre_title + ","
    
        # Create list of actors
        movie_people = movies_people.filter(movie_id=movie.movie_id)

        for person in movie_people:
            cast += person.person_id.name + ","
        
        data.append([movie_id, title, genres, cast, plot])
    
    df = pd.DataFrame(data, columns = ['Movie_ID','Title', 'Genres', 'Cast', 'Plot'])

    df = clean_data(df)
    final_df = create_bag_of_words(df)

    # instantiating and generating the count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(final_df['bag_of_words'])

    # generating the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    return final_df, cosine_sim

def recommendations(df, iden, cosine_sim):
    indices = pd.Series(df.index)

    # initializing the empty list of recommended movies
    recommended_movies = []
    
    # getting the index of the movie that matches the title
    idx = indices[indices == iden].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        recommended_movies.append(list(df.index)[i])
        
    return recommended_movies

def create_bag_of_words(df):
    data = []

    for index, row in df.iterrows():
        bag_of_words = row['Genres'].strip() + " "  + row['Cast'].strip() + " " + row['Key_words'].strip()

        data.append([row['Movie_ID'], row['Title'], bag_of_words])
    
    new_df = pd.DataFrame(data, columns=['Movie_ID', 'Title', 'bag_of_words'])
    new_df.set_index('Movie_ID', inplace=True, drop=True)

    return new_df

def clean_data(df):
    # initializing the new column
    df['Key_words'] = ""

    for index, row in df.iterrows():
        plot = row['Plot']
        
        # instantiating Rake, by default it uses english stopwords from NLTK
        # and discards all punctuation characters as well
        r = Rake()

        # extracting the words by passing the text
        r.extract_keywords_from_text(plot)

        # getting the dictionary with key words as keys and their scores as values
        key_words_dict_scores = r.get_word_degrees()

        key_words = ""

        for key in list(key_words_dict_scores.keys()):
            key_words += key + " "

        # Clean genre and cast data
        genres = clean_genres(row['Genres'].split(","))
        cast = clean_actors(row['Cast'].split(","))

        # Assign all cleaned data to designated column
        df.loc[index, 'Key_words'] = key_words
        df.loc[index, 'Genres'] = genres
        df.loc[index, 'Cast'] = cast


    # dropping the Plot column
    df.drop(columns = ['Plot'], inplace = True)

    return df

def clean_actors(actors):
    cast = ""
    for actor in actors:
        # Merge into one word and make lower case
        cast += actor.replace(" ", "").lower() + " "

    return cast

def clean_genres(genres):
    cleaned_genres = ""
    for genre in genres:
        # Make lower case
        cleaned_genres += genre.lower() + " "

    return cleaned_genres

# Converts suggestion list of ids into suggestion list of movie objects
def get_related(related_ids):
    related = []
    
    for movie_id in related_ids:
        rec_movie = Movie.objects.get(movie_id=movie_id)
        # only add recommendation if not already in recommendation list
        if (rec_movie not in related):
            related.append(rec_movie)

    return related

def search_actors(query, explore):
    actors = Person.objects.filter(name__icontains=query)
    
    movies_actors = []
    
    for actor in actors:
        explore.append((actor.name, actor.person_id, 'actor'))
        # Actor can be in more than one movie, iterate through each actors movies
        for movie_person in MoviePerson.objects.filter(person_id=actor.person_id):
            movie = Movie.objects.get(movie_id=movie_person.movie_id.movie_id)
            if movie not in movies_actors:
                movies_actors.append(movie)

    return movies_actors, explore

def search_genres(query, explore):
    genres = Genre.objects.filter(genre_title__icontains=query)
    
    movies_genres = []
    
    for genre in genres:
        explore.append((genre.genre_title, genre.genre_id, 'genre'))
        # More than one movie can have same genre
        for genre_movie in MovieGenre.objects.filter(genre_id=genre.genre_id):
            movie = Movie.objects.get(movie_id=genre_movie.movie_id.movie_id)
            if movie not in movies_genres:
                movies_genres.append(movie)
    
    return movies_genres, explore

def get_suggestions(suggestion_type, suggestion_id, df, cosine_sim, genres):
    if suggestion_type == 'actor':
        suggestion_title = Person.objects.get(person_id=suggestion_id).name
        
        actor_movies = []
        suggested_movies = []
        unsorted_suggested = []

        # Get all movies that actor is in
        for movie_person in MoviePerson.objects.filter(person_id=suggestion_id):
            movie = Movie.objects.get(movie_id=movie_person.movie_id.movie_id)
            actor_movies.append(movie)
            suggested_movies.append(movie)

        # Get related movies for each movie that actor is in 
        for movie in actor_movies:
            suggestions = recommendations(df, movie.movie_id, cosine_sim)
            
            # Converts suggestion list of ids into suggestion list of movie objects
            all_suggestions = get_related(suggestions)
            
            # Add to suggestion list if not already in
            for mov in all_suggestions:
                if mov not in unsorted_suggested:
                    unsorted_suggested.append(mov)
        
        # Sort suggestion list by user favourite genres
        sorted_suggested = sort_by_user_genre(suggestion_title,unsorted_suggested, genres)

        # Add to suggestion list if not already in there
        for movie in sorted_suggested:
            if movie not in suggested_movies:
                suggested_movies.append(movie)

    elif suggestion_type == 'genre':
        suggestion_title = Genre.objects.get(genre_id=suggestion_id).genre_title

        suggested_movies = []

        # Get all movies with genre
        for genre_movie in MovieGenre.objects.filter(genre_id=suggestion_id):
            movie = Movie.objects.get(movie_id=genre_movie.movie_id.movie_id)
            suggested_movies.append(movie)
    else:
        movie = Movie.objects.get(movie_id=suggestion_id)
        suggestion_title = movie.title.strip()

        # Get all suggestions for movie (movie ids)
        suggestions = recommendations(df, int(suggestion_id), cosine_sim)

        # Converts suggestion list of ids into suggestion list of movie objects
        suggested_movies = get_related(suggestions)

        # Sorts suggested movies by user favourite genre
        suggested_movies = sort_by_user_genre(suggestion_title, suggested_movies, genres)

        # Adds original movie to suggestion list
        suggested_movies.insert(0,movie)

    return suggested_movies, suggestion_title

def sort_by_user_genre(query, movies, genres):
    if (genres):
        user_genres = genres.strip(",").split(",")
    else:
        user_genres = []
    movie_genre_list = []

    # Get genres for movies in list
    for movie in movies:
        movie_genre = MovieGenre.objects.all().filter(movie_id=movie.movie_id)
        weight = 0

        for genre in movie_genre:
            genre_title = Genre.objects.all().get(genre_id=genre.genre_id.genre_id).genre_title

            # Increase weight by 1 each time user fav genre found in the movie's list of genres
            if genre_title in user_genres:
                weight += 1

        # List of (movie, weight) tuples
        movie_genre_list.append((movie,weight))

    # Sort based on weight
    sort = sorted(movie_genre_list, key=lambda x: x[1], reverse=True)

    print("Sorted for " + query + ":")
    print (sort)
    print()
    sorted_movies = []

    # Return list of sorted movies without weight
    for movie in sort:
        sorted_movies.append(movie[0])

    return sorted_movies
