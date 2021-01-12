# calculate avg ratings
from movie.models import Movie, RatedReview

all_movies = Movie.objects.all()
for m in all_movies:
    associated_reviews = m.review_by_movies.all()
    all_ratings = [m.rating for m in associated_reviews]
    if len(all_ratings):
        m.dAvgRating = sum(all_ratings) / len(all_ratings)
        m.numberReviews += len(all_ratings)
        m.save()
