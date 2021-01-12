from django.shortcuts import render
from movie.models import Movie
from collections import defaultdict

# Create your views here.

# show all directors in our database
def directors(request):
    movie_list = Movie.objects.all()
    director_dict = movie_list.order_by().values('directors').distinct()
    director_list = []
    for director in director_dict:
        director_list += director['directors'].split(",")
    director_list = sorted(director_list)
    director_dic = defaultdict(list)
    for d in director_list:
        director_dic[d[0]].append(d)

    context = {
        "director_dic": dict(director_dic),
    }
    return render(request, "directors/directors.html", context)
