from movie.models import Movie
from accounts.models import Wishlist
from django.contrib.auth.models import User
import random

all_users = User.objects.all()
all_movies = Movie.objects.all()
count = 0

for user in all_users:
    for movie in all_movies:
        # roll the dice
        if (random.randint(1, 100) == 100) and (not Wishlist.objects.filter(user=user, movie=movie).exists()):
            wishList = Wishlist(movie=movie, 
                user= user,
                )
            wishList.save()
            count += 1
print(f"I added total of {count} wishlists, did I do a good job? ")