from movie.models import Movie, RatedReview
from django.contrib.auth.models import User
import random



# for i in range(500):
#     user = User(username=f'testuser{i}', email=f'testuser{i}@filmfinder', password=f'testuser{i}madebyme',
#     is_superuser=False, is_staff=False)
#     user.save()


all_users = User.objects.all()
all_movies = Movie.objects.all()
review_count = 0

for user in all_users:
    for movie in all_movies:
        # roll d6
        if (random.randint(1, 6) == 6) and (not RatedReview.objects.filter(user=user, movie=movie).exists()):
            rating = random.randint(0, 5)
            review = f"I'm a bot. I decide {user.username} rates the movie {movie.title} as {rating} out of 5. "
            ratedReview = RatedReview(movie=movie, 
                user= user, 
                rating=rating,
                review=review,
                )
            ratedReview.save()
            review_count += 1
print(f"I added total of {review_count} reviews, did I do a good job? ")

