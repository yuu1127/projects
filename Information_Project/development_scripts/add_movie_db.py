from movie.models import Movie
from imdb import IMDb, IMDbError
import imdb.helpers
import requests
from bs4 import BeautifulSoup as bs
import time

IMDB_POP_URL = "https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&view=simple&start="

"""
info provided by main
['original title', 'cast', 'genres', 'runtimes', 'countries', 'country codes',
'language codes', 'color info', 'aspect ratio', 'sound mix', 'box office',
'certificates', 'original air date', 'rating', 'votes', 'cover url', 'imdbID',
'plot outline', 'languages', 'title', 'year', 'kind', 'directors', 'writers',
'producers', 'composers', 'cinematographers', 'editors', 'editorial department',
'casting directors', 'production designers', 'art directors', 'set decorators',
'costume designers', 'make up department', 'production managers', 'assistant directors',
'art department', 'sound department', 'special effects', 'visual effects', 'stunts',
'camera department', 'casting department', 'costume departmen', 'location management',
'music department', 'script department', 'transportation department', 'miscellaneous',
'thanks', 'akas', 'writer', 'director', 'top 250 rank', 'production companies',
'distributors', 'special effects companies', 'other companies']
"""

try:
    ia = IMDb()
    # tops = ia.get_top250_movies()
    pops = ia.get_popular100_movies()
except IMDbError as e:
    print(e)

# for t in pops:
#     try:
#         ia.update(t, ['main'])
#     except IMDbError as e:
#         print(e)
#     if not Movie.objects.filter(imdbID=t['imdbID']).exists():
#         directors_list = []
#         genres_list = []
#         cast_list = []
#         for d in t['directors']:
#             directors_list.append(d['name'])
#         for g in t['genres']:
#             genres_list.append(g)
#         for c in t['cast']:
#             cast_list.append(c['name'])
#         record = Movie(title=t['title'],
#                     directors=','.join(directors_list),
#                     genres=','.join(genres_list),
#                     cast=','.join(cast_list),
#                     year=t['year'],
#                     imdbID=t['imdbID'],
#                     coverUrl=imdb.helpers.fullSizeCoverURL(t),
#                     plot=t.get('plot outline', ''),
#                     )
#         record.save()


for i in range(1,2501,50):
    imdb_url = IMDB_POP_URL + str(i)
    page_content = requests.get(imdb_url).content
    soup = bs(page_content, 'lxml')
    for a in soup.select('.lister-item-image a'):
        imdb_id = a['href'].split('/')[2][2:]
        t = ia.get_movie(str(imdb_id))
        if not Movie.objects.filter(imdbID=t['imdbID']).exists():
            directors_list = []
            genres_list = []
            cast_list = []
            for d in t['directors']:
                directors_list.append(d['name'])
            for g in t['genres']:
                genres_list.append(g)
            for c in t['cast']:
                cast_list.append(c['name'])
            record = Movie(title=t['title'],
                        directors=','.join(directors_list),
                        genres=','.join(genres_list),
                        cast=','.join(cast_list),
                        year=t['year'],
                        imdbID=t['imdbID'],
                        coverUrl=imdb.helpers.fullSizeCoverURL(t),
                        plot=t.get('plot outline', ''),)
            record.save()
    time.sleep(20)
