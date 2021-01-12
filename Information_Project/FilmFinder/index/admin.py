from django.contrib import admin
from movie.models import Movie, RatedReview
from accounts.models import BanList, Wishlist
# Register your models here.

admin.site.register(Movie)
admin.site.register(RatedReview)
admin.site.register(BanList)
admin.site.register(Wishlist)
