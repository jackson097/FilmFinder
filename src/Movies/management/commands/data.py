from django.core.management.base import BaseCommand, CommandError
import csv, requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

from Movies.models import Movie, MovieGenre, MoviePerson
from Genres.models import Genre
from filmFinder.settings import tmbd_api_key
from Reception.models import Reception
from Background.models import Background
from Person.models import Person

api_key = tmbd_api_key

class Command(BaseCommand):
    help = 'Script to import Imdb data into tables'

    def handle(self, *args, **options):
        ########## importing title basics into appropiate tables.
        with open('data/movie_data.csv', "r", newline='') as myfile: 
            # next(myfile)
            # head = [next(myfile) for x in range(len(myfile.readlines()))]
            reader = csv.reader(myfile)
            for row in reader:
                temp_id = row[4]
                poster_url = row[2]
                overview = row[3]
                title = row[1]
                numRatings = row[6].replace(",", "")
                duration = row[7]
                backdrop = row[8]
                release = row[9]
                actors = row[10].strip("[]").strip("")
                genres = row[11].strip("[]").strip("")

                Moviecreated, created = Movie.objects.get_or_create(title=title, image=poster_url, overview=overview, temp_id=temp_id, backdrop=backdrop)
                _, ReceptionCreated = Reception.objects.get_or_create(movie_id=Moviecreated, avgRatings=row[5], numRatings=int(numRatings))
                _, BackgroundCreated = Background.objects.get_or_create(movie_id=Moviecreated, releaseDate=release, length=duration)

                for genre in genres.split(", "):
                    Genrecreated, created = Genre.objects.get_or_create(genre_title=genre.strip("/'"))
                    if Genrecreated.genre_title in genres:
                        _, movieGenreCreated = MovieGenre.objects.get_or_create(movie_id=Moviecreated, genre_id=Genrecreated)

                for actor in actors.split(", "):
                    Personcreated, created = Person.objects.get_or_create(name=actor.strip("/'"))
                    if Personcreated.name in actors:
                        _, moviePersonCreated = MoviePerson.objects.get_or_create(movie_id=Moviecreated, person_id=Personcreated)
                        print("title: {}, person: {}".format(title, Personcreated.name))

                