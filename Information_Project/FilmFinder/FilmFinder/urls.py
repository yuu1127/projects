"""FilmFinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from index import views as inviews


urlpatterns = [
    # disable admin page
    # path('admin/', admin.site.urls),
    # homepage: browse all movies
    path('', inviews.index, name='index'),
    # user accounts management, including wishlist and blocklist features
    path('accounts/', include('accounts.urls'), name='account'),
    # movie detail pages
    path('movie/', include('movie.urls'), name='movie'),
    # search for movies feature
    path('search/', include('search.urls'), name='search'),
    # support for login using social network accounts using django.allauth
    path('social_accounts/', include('allauth.urls')),
    # shows all directors
    path('directors/', include('directors.urls'), name='directors'),
]
