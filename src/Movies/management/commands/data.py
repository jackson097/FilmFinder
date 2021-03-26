from django.core.management.base import BaseCommand, CommandError
import csv, requests
from Movies.models import Movie, MovieGenre
from filmFinder.settings import tmbd_api_key

api_key = tmbd_api_key

class Command(BaseCommand):
    help = 'Script to import Imdb data into tables'

    def handle(self, *args, **options):
        # importing title basics into appropiate tables. 
        response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=' +  api_key + '&primary_release_year=2017&sort_by=revenue.desc')
        print(response)
        with open('data/movies_metadata.csv', "r", encoding="utf-8") as myfile: 
            next(myfile)
            head = [next(myfile) for x in range(100)]
            reader = csv.reader(head)
            for row in reader:
                line = row[1].split(":")
                title = row[8]
                poster_url = "https://image.tmdb.org/t/p/w500" + row[11]
                # print(title)
                # print(title)
                # Moviecreated, created = Movie.objects.get_or_create(title=title, image=poster_url)
                # _, created = MovieGenre.objects.get_or_create(movie_id=Moviecreated, genre_id=row[0])