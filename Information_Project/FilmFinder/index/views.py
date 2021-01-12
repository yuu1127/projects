from django.shortcuts import render
from movie.models import Movie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from helper import get_banlist_movies

# list of all the genres in our database 
genre_list = ['Fantasy', 'Mystery', 'Sport', 'History', 'Biography', 'Crime', 'Sci-Fi', 'Film-Noir', 'Western', 'Animation',
              'Romance', 'War', 'Family', 'Thriller', 'Documentary', 'Musical', 'Comedy', 'Drama', 'Horror', 'Music', 'Adventure', 'Action']


# top 10 directors from IMDb
top_director_list = ['Stanley Kubrick', 'Alfred Hitchcock', 'David Fincher', 'Christopher Nolan', 'Martin Scorsese',
                     'Quentin Tarantino', 'Sergio Leone', 'Francis Ford Coppola', 'Sidney Lumet', 'Milos Forman']
# Create your views here.


# homepage movie browse
def index(request):
    banned_movies = get_banlist_movies(request)
    query_string = ''
    genre = request.GET.get('genre')
    director = request.GET.get('director')
    rating = request.GET.get('rating')
    if genre:
        query_string += '&genre={0}'.format(genre)
        movie_list = Movie.objects.filter(genres__contains=genre)
    elif director:
        query_string += '&director={0}'.format(director)
        movie_list = Movie.objects.filter(directors__contains=director)
    elif rating:
        query_string += '&rating={0}'.format(rating)
        min_rating = float(rating.split(' - ')[0])
        max_rating = float(rating.split(' - ')[1])
        movie_list = [movie for movie in Movie.objects.all() if movie.average_rating(
            banned_movies) >= min_rating and movie.average_rating(banned_movies) <= max_rating]
    else:
        movie_list = Movie.objects.all()
    # sort movie by their average ratings, if average rating is the same, sort by movie title
    movie_list = sorted(movie_list, key=lambda movie: (
        movie.average_rating(banned_movies) * - 1, movie.title))
    # paginator
    page = request.GET.get('page', 1)
    # show 12 movies per page
    paginator = Paginator(movie_list, 12)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    context = {
        "movies": movies,
        "query_string": query_string,
        "genre_list": genre_list,
        "director_list": top_director_list,
        "ban_list": banned_movies,
    }

    return render(request, "index/index.html", context)
