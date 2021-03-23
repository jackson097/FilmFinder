from django.core.management.base import BaseCommand, CommandError
import csv
from Movies.models import Movie, MovieGenre

class Command(BaseCommand):
    help = 'Script to import Imdb data into tables'

    def handle(self, *args, **options):
        # importing title basics into appropiate tables. 
        with open('data/title_basics.csv', "r", encoding="utf-8") as myfile: 
            next(myfile)
            head = [next(myfile) for x in range(10)]
            reader = csv.reader(head)
            for row in reader:
                Moviecreated, created = Movie.objects.get_or_create(movie_id=row[0], title=row[2])
                _, created = MovieGenre.objects.get_or_create(movie_id=Moviecreated, genre_id=row[0])