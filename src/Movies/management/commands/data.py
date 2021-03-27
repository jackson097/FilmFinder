from django.core.management.base import BaseCommand, CommandError
import csv, requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

from Movies.models import Movie, MovieGenre
from filmFinder.settings import tmbd_api_key
from Reception.models import Reception
from Background.models import Background

api_key = tmbd_api_key

class Command(BaseCommand):
    help = 'Script to import Imdb data into tables'

    def handle(self, *args, **options):
        ########## importing title basics into appropiate tables.
        with open('data/movie_data.csv', "r", newline='') as myfile: 
            next(myfile)
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
                # print(overview)
                # print(release)
                Moviecreated, created = Movie.objects.get_or_create(title=title, image=poster_url, overview=overview, temp_id=temp_id, backdrop=backdrop)
                _, ReceptionCreated = Reception.objects.get_or_create(movie_id=Moviecreated, avgRatings=row[5], numRatings=int(numRatings))
                _, BackgroundCreated = Background.objects.get_or_create(movie_id=Moviecreated, releaseDate=release, length=duration)
                # _, created = MovieGenre.objects.get_or_create(movie_id=Moviecreated, genre_id=row[0])

        ####### creating csv data
        # row_names = ['movie_id', 'movie_url']
        # with open('data/movie_url.csv', 'r', newline='') as in_csv:
        #     head = [next(in_csv) for x in range(10)]
        #     reader = csv.DictReader(head, fieldnames=row_names, delimiter=',')
        #     for row in reader:
        #         movie_id = row['movie_id']
        #         movie_url = row['movie_url']
        #         domain = 'http://www.imdb.com'
        #         with urllib.request.urlopen(movie_url) as response:
        #             html = response.read()
        #             soup = BeautifulSoup(html, 'html.parser')
        #             # Get url of poster image
        #             try:
        #                 image_url = soup.find('div', class_='poster').a.img['src']
        #                 # TODO: Replace hardcoded extension with extension from string itself
        #                 extension = '.jpg'
        #                 image_url = ''.join(image_url.partition('_')[0]) + extension
        #                 filename = 'img/' + movie_id + extension
        #                 description = soup.find('div', class_='summary_text').get_text()
        #                 title = soup.find('div', class_='title_wrapper').h1.get_text()
        #                 imdbID = soup.find('div', class_='imdbRating').a['href'].split('/')[2]
        #                 avgRating = soup.find('div', class_='ratingValue').strong.span.get_text()
        #                 numRating = soup.find('div', class_='imdbRating').a.span.get_text()
        #                 duration = soup.find('div', class_='subtext').time.get_text()
        #                 backdrop = soup.find('div', class_='slate').a.img['src']
        #                 releaseDate = soup.find('div', class_='title_wrapper').h1.span.a.get_text()
        #                 ##trying to get backdropimage by getting another image from the gallery
        #                 # backdropimage = soup.find('div', class_='mediastrip').content

        #                 # with urllib.request.urlopen(image_url) as response:
        #                 #     with open(filename, 'wb') as out_image:
        #                 #         out_image.write(response.read())
        #                 # print(releaseDate)
        #                 with open('data/movie_data.csv', 'a', newline='') as out_csv:
        #                     writer = csv.writer(out_csv, delimiter=',')
        #                     writer.writerow([movie_id, title[:-7], image_url, str(description).strip(), imdbID, avgRating, numRating, str(duration).strip(), backdrop, releaseDate])
        #             # Ignore cases where no poster image is present
        #             except AttributeError:
        #                 pass