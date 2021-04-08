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

def recommendations(df, id, cosine_sim):
    indices = pd.Series(df.index)

    # initializing the empty list of recommended movies
    recommended_movies = []
    
    # getting the index of the movie that matches the title
    idx = indices[indices == id].index[0]

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
        