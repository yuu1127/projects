from accounts.models import BanList
from movie.models import RatedReview


def get_banlist_movies(request):
    result_dict = {}
    banlist = BanList.objects.none()
    if request.user.is_authenticated and BanList.objects.filter(user=request.user).exists():
        banlist = BanList.objects.filter(user=request.user)
    all_reviews = RatedReview.objects.none()
    for b in banlist:
        reviewed_movies = b.blockedUser.review_by_users.all()
        all_reviews = all_reviews | reviewed_movies
    for r in all_reviews:
        # print(r.user.username, r.rating, r.movie.imdbID)
        result_dict.setdefault(r.movie.imdbID, []).append(r.rating)
    return result_dict

# mode: 0 review add, 1 review edit, 2 review remove


def update_dAvgRating(movie, mode):
    associated_reviews = movie.review_by_movies.all()
    all_ratings = [m.rating for m in associated_reviews]
    if mode == 0:
        movie.numberReviews += 1
    elif mode == 2:
        movie.numberReviews -= 1
    movie.dAvgRating = sum(all_ratings) / movie.numberReviews
    movie.save()
