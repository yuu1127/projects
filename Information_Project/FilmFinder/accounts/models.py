from django.db import models
from django.contrib.auth.models import User
from movie.models import Movie

# Create your models here.


# model for wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='wishlist_owner')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='wishlist_movies')


# model for blocklist
class BanList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='banlist_owner')
    blockedUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='banlist_banned')
