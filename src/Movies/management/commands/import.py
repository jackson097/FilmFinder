from django.core.management.base import BaseCommand, CommandError
import csv, requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

class Command(BaseCommand):
    help = 'Script to import Imdb data into tables'

    def handle(self, *args, **options):
        row_names = ['movie_id', 'movie_url']
        with open('data/movie_url.csv', 'r', newline='') as in_csv:
            head = [next(in_csv) for x in range(10)]
            reader = csv.DictReader(head, fieldnames=row_names, delimiter=',')
            for row in reader:
                movie_id = row['movie_id']
                movie_url = row['movie_url']
                domain = 'http://www.imdb.com'
                with urllib.request.urlopen(movie_url) as response:
                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    # Get url of poster image
                    try:
                        
                        image_url = soup.find('div', class_='poster').a.img['src']
                        # TODO: Replace hardcoded extension with extension from string itself
                        extension = '.jpg'
                        image_url = ''.join(image_url.partition('_')[0]) + extension
                        filename = 'img/' + movie_id + extension
                        description = soup.find('div', class_='summary_text').get_text()
                        title = soup.find('div', class_='title_wrapper').h1.get_text()
                        imdbID = soup.find('div', class_='imdbRating').a['href'].split('/')[2]
                        avgRating = soup.find('div', class_='ratingValue').strong.span.get_text()
                        numRating = soup.find('div', class_='imdbRating').a.span.get_text()
                        duration = soup.find('div', class_='subtext').time.get_text()
                        backdrop = soup.find('div', class_='slate').a.img['src']
                        releaseDate = soup.find('div', class_='title_wrapper').h1.span.a.get_text()
                        actorsRow = soup.find('div', class_='plot_summary').find_all('div')[3].find_all('a')
                        actors = []
                        for actor in actorsRow:
                            actors.append(actor.get_text())
                        actors = actors[:-1]
                        print(actors)

                        with open('data/movie_data.csv', 'a', newline='') as out_csv:
                            writer = csv.writer(out_csv, delimiter=',')
                            writer.writerow([movie_id, title[:-7], image_url, str(description).strip(), imdbID, avgRating, numRating, str(duration).strip(), backdrop, releaseDate, actors])
                   
                    # Ignore cases where no poster image is present
                    except AttributeError:
                        pass