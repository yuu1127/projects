from django.shortcuts import render
from movie.models import Movie
from django.http import Http404
import re
from helper import get_banlist_movies


# Create your views here.


# search for movie feature
def search_results(request):
    if not request.GET.get('q'):
        raise Http404("query not found")
    ban_list = get_banlist_movies(request)
    query = request.GET.get('q').strip()

    if not query or not any(c.isalpha() for c in query):
        return render(request, "search/search_results.html", {
            "ban_list": ban_list,
            "results": [],
        })
    des_inter_q = Movie.objects.none()
    # matching by movie title
    q_title = Movie.objects.filter(title__icontains=query)
    # matching by movie genre
    q_genres = Movie.objects.filter(genres__icontains=query)

    # matching by movie plot, keywords can have different order with movie plot
    for q in query.split():
        q_des = Movie.objects.filter(plot__iregex=r'\b{0}\b'.format(q))
        if len(des_inter_q) == 0:
            des_inter_q = q_des
        else:
            des_inter_q = des_inter_q.intersection(q_des)

    q_union = q_title.union(q_genres, des_inter_q)

    movie_list = sorted(
        q_union, key=lambda movie: movie.average_rating(ban_list), reverse=True)

    if len(q_union) > 0:
        return render(request, "search/search_results.html", {
            "results": movie_list,
            "ban_list": ban_list,
        })

    return render(request, "search/search_results.html", {
        "ban_list": ban_list,
        "results": [],
    })
