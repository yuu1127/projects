from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from .models import Movie, RatedReview, RatedReviewForm
import datetime
from accounts.models import Wishlist
from collections import defaultdict
from helper import get_banlist_movies, update_dAvgRating


# list of all the genres in our database

genre_list = ['Fantasy', 'Mystery', 'Sport', 'History', 'Biography', 'Crime', 'Sci-Fi', 'Film-Noir', 'Western', 'Animation',
              'Romance', 'War', 'Family', 'Thriller', 'Documentary', 'Musical', 'Comedy', 'Drama', 'Horror', 'Music', 'Adventure', 'Action']

# Create your views here.


# movie detail page
def display_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    ban_list = get_banlist_movies(request)
    associated_reviews = movie.review_by_movies.all()
    reviewed = False
    wishlist_included = False

    # if user is logged in, check the user's wishlist and blocklist
    if request.user.is_authenticated:
        wishlist_included = Wishlist.objects.filter(
            user=request.user, movie=movie).exists()
        reviewed = RatedReview.objects.filter(
            user=request.user, movie=movie).exists()
        all_reviewed_users = [x.user for x in associated_reviews]
        all_banned_users = [
            x.blockedUser for x in request.user.banlist_owner.all()]
        banned_and_reviewed = [
            x for x in all_reviewed_users if x in all_banned_users]
        # do not display the reviews made by the users that are blocked
        for br in banned_and_reviewed:
            associated_reviews = associated_reviews.exclude(user=br)

    # movie recommendations return 5 similar movies based on differnet criteria 
    # use set since movie recommended by genre and director could be same
    similar_movies_reviews = set()
    similar_movies_genres = set()
    similar_movies_directors = set()
    similar_movies_casts = set()
    movie_list = Movie.objects.all()

    # recommendation by other reviews:
    other_reviewers = []
    if request.user.is_authenticated:
        review_exist = associated_reviews.filter(
            user=request.user, rating__gte=4)
        if review_exist.count() > 0:
            for review in associated_reviews:
                if review.user != request.user and review.rating >= 4:
                    other_reviewers.append(review.user)
            for reviewer in other_reviewers:
                reviewer_similar_movies = RatedReview.objects.filter(
                    user=reviewer, rating__gte=4).exclude(movie=movie)
                for mv in reviewer_similar_movies:
                    similar_movies_reviews.add(mv.movie)
    if len(similar_movies_reviews) > 5:
        similar_movies_reviews = random.sample(similar_movies_reviews, 5)

    # recommendation by genre
    genres = []
    pre_genres = sorted(genre_list)
    pre_genres = map(lambda x: x.lower(), pre_genres)
    index = 0
    movie_index = 0
    for m in movie_list:
        genres.append(m.genres)
        if m.imdbID == movie.imdbID:
            movie_index = index
        index += 1
    cv = CountVectorizer(vocabulary=pre_genres)
    X = cv.fit_transform(genres).toarray()
    similarities = cosine_similarity(X)
    similarity_values = pd.Series(similarities[movie_index])
    # show similarity and index
    similarity_values = list(
        similarity_values.sort_values(ascending=False).index)
    # put top5 similar genre movies in set
    for i in similarity_values[:5]:
        if movie.title != movie_list[i].title:
            similar_movies_genres.add(movie_list[i])
    
    director_movies = set()
    # recommendation by director
    director = movie.directors
    # for each director take movies
    directors = list(director.split(","))
    for di in directors:
        movies = Movie.objects.filter(
            directors__contains=di).exclude(imdbID=movie.imdbID)
        for mv in movies:
            director_movies.add(mv)
    if len(director_movies) > 5:
        director_movies = random.sample(director_movies, 5)
    for d in director_movies:
        similar_movies_directors.add(d)

    casts = list(movie.cast.split(","))
    cast_point = defaultdict(int)
    index = 0
    for m in movie_list:
        if m.imdbID != movie.imdbID:
            for c in list(m.cast.split(",")):
                if c in casts:
                    cast_point[index] += 1
        index += 1

    for key, value in sorted(cast_point.items(), key=lambda item: item[1], reverse=True)[:5]:
        similar_movies_casts.add(movie_list[key])

    associated_reviews = sorted(
        associated_reviews, key=lambda review: review.cDate, reverse=True)
    # if reviewed by current user, pre-fill the contents
    if reviewed:
        selected_review = RatedReview.objects.get(
            user=request.user, movie=movie)
        form = RatedReviewForm(instance=selected_review)
    else:
        form = RatedReviewForm()
    return render(request, "movie/movie_details.html", {
        "movie": movie, # current movie object
        "form": form, # rating and review form
        "asso_reviews": associated_reviews, # all reviews associated with current movie
        "reviewed": reviewed, # if current movie is reviewed by current user 
        "similar_movies_reviews": similar_movies_reviews,
        "similar_movies_genres": similar_movies_genres,
        "similar_movies_directors": similar_movies_directors,
        "similar_movies_casts": similar_movies_casts,
        "included": wishlist_included, # if current movie is included in current user's wishlist
        "ban_list": ban_list, # current user's blocklist content
    })


# leave a review for current movie
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    form = RatedReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        review = form.cleaned_data['review']
        ratedReview = RatedReview(movie=movie,
                                  user=request.user,
                                  rating=rating,
                                  review=review,
                                  )
        ratedReview.save()
        update_dAvgRating(movie, 0)
        return HttpResponseRedirect(reverse('movie:movie_detail', args=(movie_id,)))
    return render(request, 'movie/movie_details.html', {'movie': movie, 'form': form})


# edit or delete current user's review
def edit_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    selected_review = RatedReview.objects.get(user=request.user, movie=movie)
    if request.method == 'POST' and 'review_save' in request.POST:
        form = RatedReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            review = form.cleaned_data['review']
            selected_review.rating = rating
            selected_review.review = review
            selected_review.cDate = datetime.date.today()
            selected_review.save()
            update_dAvgRating(movie, 1)
            return HttpResponseRedirect(reverse('movie:movie_detail', args=(movie_id,)))
        return render(request, 'movie/movie_details.html', {'movie': movie, 'form': form})
    elif request.method == 'POST' and 'review_delete' in request.POST:
        selected_review.delete()
        update_dAvgRating(movie, 2)
        return HttpResponseRedirect(reverse('movie:movie_detail', args=(movie_id,)))
