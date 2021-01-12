from django.db import models
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
import datetime

# Create your models here.


# all info about a movie
class Movie(models.Model):
    imdbID = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    directors = models.CharField(max_length=64)
    genres = models.CharField(max_length=64)
    year = models.IntegerField()
    coverUrl = models.CharField(max_length=64)
    plot = models.TextField()
    cast = models.TextField()
    dAvgRating = models.FloatField(default=0)
    numberReviews = models.IntegerField(default=0)

    def __str__(self):
        return f"Movie name: {self.title}"

    def cast_as_list(self):
        return self.cast.split(",")

    def genres_as_list(self):
        return self.genres.split(",")

    def directors_as_list(self):
        return self.directors.split(",")

    def average_rating(self, banned):
        # dAvgRating is the default rating without blocklist
        avg_rating = self.dAvgRating
        num_reviews = self.numberReviews
        # check if blocklist is not empty
        # and current movie is reviewed by one of the blocked users
        if banned and (self.imdbID in banned):
            # if all the reviews are made by one of the blocked users
            if num_reviews == len(banned[self.imdbID]):
                avg_rating = 0
            else:
                # recalculate the average rating
                rating_list = banned[self.imdbID]
                for r in rating_list:
                    avg_rating = (avg_rating * num_reviews - r) / \
                        (num_reviews - 1)
                    num_reviews = num_reviews - 1
        return round(avg_rating, 1)


# user's ratings and review stores in this model
class RatedReview(models.Model):
    RATING_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review_by_users')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='review_by_movies')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.CharField(max_length=500)
    cDate = models.DateField(_("Date"), default=datetime.date.today)


# use ModelForm for quick deployment
class RatedReviewForm(ModelForm):
    class Meta:
        model = RatedReview
        fields = ['rating', 'review']
        help_texts = {
            'review': _('Maximum 500 characters.'),
        }
        widgets = {
            'review': Textarea()
        }
