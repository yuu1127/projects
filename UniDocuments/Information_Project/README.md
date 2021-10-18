# COMP9900-H12A-0xdeadbeef

## Python environment 
- Python3
- Run `pip install -r requirements.txt` to install required packages

## What's working now
1. user register, login, logout, change password and password reset
2. user login using google, facebook or twitter account
3. home page with movie display, filter by genres, directors and average ratings
4. search by title, description and genres
5. user can review and rating a movie, eidt the review and delete the review
6. user can have a wishlish with the movies they would like to watch
7. user can have a banlist with banned users, review and average ratings change accordingly
8. Recommendations of similar movies 

## Django
[Django](https://www.djangoproject.com) is a backend web application framework that integrate database and user management. It is Python-based and follows the model-template-views architectural pattern.
1. Installation
`pip install django`
2. Create a Django project: `django-admin startproject FilmFinder`
	1. Already done
	2. After creation, Django will automatically has the following structure (as shown in the master branch):
	
```
	FilmFinder/
    manage.py
    FilmFinder/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```	

3. Start the server: `python3 manage.py runserver`
	- It should display a Django landing page on `http://127.0.0.1:8000/`
4. Create an app: `python3 manage.py startapp index`
	1. Create an app called index as shown in this branch
	2. An app in Django, it is a feature, usually represented by sub-domains. For example, I want to display all the movies in the front page and I created the index app to do this.
	3. After creating a new app, check if it is exist in the `settings.py`, if not, add it in the `INSTALLED_APPS` section of the `settings.py`
	4. In the `urls.py`of the project, add the url section for the new app:
		1. There are two ways to do it, the first way is like the following. It includes all the urls of polls to the `/polls` sub-domain.
		
```python
from django.contrib import admin
from django.urls import include, path

	urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```
		2. Or you if the number of the web pages for the new app is small, you can use something like I did.
			
```python
from django.contrib import admin
from index import views as inviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inviews.index, name='index'),
]
```

5. Add `'DIRS': [BASE_DIR / 'templates']` in settings
	- I create a templates folder all the html pages for each app. There are different approaches but I like to put all the htmls in one place
	
6. Database:
	1. The default database system for Django, which is we use, is SQLite
	2. Database tables are represented as models in Dajango
	3. Each app has a `models.py`. You can create tables there. For example:
	
```python
	from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=64)
    directors = models.CharField(max_length=64)
    genres = models.CharField(max_length=64)
    year = models.IntegerField()
    imdbID = models.IntegerField()

    def __str__(self):
        return f"Movie name: {self.title}\nDirector: {self.directors}\nGenres: {self.genres}\nYear: {self.year}\nimdbID: {self.imdbID}"
```

	4. After the creation we need to sync it with the database:
		1. `$ python3 manage.py migrate` 
		2. `$ python3 manage.py migrate --run-syncdb`
7. Create a super user: `python3 manage.py createsuperuser`
8. Run scrip in shell:
	1. Django includes a Python shell so that you can write scripts. I used this shell to run my `add_db.py` script.
	2. `python manage.py`
	3. `$ python manage.py shell < add_db.py`
	
## IMDbpy
[IMDbpy](https://imdbpy.github.io) is a Python package wrapper of the APIs from IMDB website. We use this package to retrieve movie data. Let’s look at the example from its website, `##` part are extra comments I made:
```python
from imdb import IMDb

# create an instance of the IMDb class
ia = IMDb()

# get a movie and print its director(s)
the_matrix = ia.get_movie('0133093')
for director in the_matrix['directors']:
    print(director['name'])

# show all information that are currently available for a movie
print(sorted(the_matrix.keys()))

# show all information sets that can be fetched for a movie
## for each data this package provides different infosets
## infosets are just categories that include different data
## the default infosets for movie object from ia.get_movie('0133093')
## are ‘main’ and ‘plot’
print(ia.get_movie_infoset())

# update a Movie object with more information
## Here we want to add the infoset ‘technical’ to our object
ia.update(the_matrix, ['technical'])
# show which keys were added by the information set
## this shows all the available information we can get
print(the_matrix.infoset2keys['technical'])
# print one of the new keys
print(the_matrix.get('tech'))
```
