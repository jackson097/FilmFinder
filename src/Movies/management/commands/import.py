from django.core.management.base import BaseCommand, CommandError
import csv, requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
from requests_html import HTMLSession

class Command(BaseCommand):
    help = 'Script to import Imdb data into tables'

    def handle(self, *args, **options):
        row_names = ['movie_id', 'movie_url']
        with open('data/movie_url.csv', 'r', newline='') as in_csv:
            head = [next(in_csv) for x in range(200)]
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

                        genres = []
                        genresRow = soup.find('div', class_='subtext').find_all('a')
                        for genre in genresRow:
                            genres.append(genre.get_text())
                        genres = genres[:-1]
                        
                        print(title)
                        # videoUrl = soup.find('div', class_='slate').a['href']
                        # videoUrl = "https://www.imdb.com/" + videoUrl
                        # video  = ""

                        # session = HTMLSession()

                        # resp = session.get(videoUrl)

                        # resp.html.render()

                        # # print(resp.html.html)

                        # with urllib.request.urlopen(resp.html.html) as vresponse:
                        #     v_html = vresponse.read()
                        #     # print(v_html)
                        #     v_soup = BeautifulSoup(v_html, 'html.parser')
                        #     try:
                        #         print("startin")
                        #         vid = v_soup.find_all('relatedVideosKey')
                        #         print(vid)

                        #     except AttributeError:
                        #         pass

                        with open('data/movie_data.csv', 'a', newline='') as out_csv:
                            writer = csv.writer(out_csv, delimiter=',')
                            writer.writerow([movie_id, title[:-7], image_url, str(description).strip(), imdbID, avgRating, numRating, str(duration).strip(), backdrop, releaseDate, actors, genres])
                        # print("{} {} {} {} {} {} {} {} {} {}".format(movie_id, title[:-7], image_url, str(description).strip(), imdbID, avgRating, numRating, str(duration).strip(), backdrop, releaseDate, actors, genres))
                    # Ignore cases where no poster image is present
                    except AttributeError:
                        pass
                    except urllib.error.HTTPError:
                        pass