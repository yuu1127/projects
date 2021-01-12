from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import NewUserForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from movie.models import Movie
from accounts.models import Wishlist, BanList
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from helper import get_banlist_movies


# show user's wishlist
def wishlist_request(request, user_name):
    selected_usr = get_object_or_404(User, username=user_name)
    ban_list = get_banlist_movies(request)
    movies_in_wishlist = selected_usr.wishlist_owner.all()
    movies_in_wishlist = sorted(
        movies_in_wishlist, key=lambda record: record.movie.average_rating(ban_list), reverse=True)
    context = {
        "selected_usr": selected_usr,
        "movies_in_wishlist": movies_in_wishlist,
        "ban_list": ban_list,
    }
    return render(request, "account/wishlist.html", context)


# remove movies from wishlist
def wishlist_remove(request, user_name, movie_id):
    selected_usr = get_object_or_404(User, username=user_name)
    selected_movie = get_object_or_404(Movie, pk=movie_id)
    previous_url = request.META.get('HTTP_REFERER')
    # authentication and make sure the movie is in the wishlist
    if request.user == selected_usr:
        if not Wishlist.objects.filter(user=selected_usr, movie=selected_movie).exists():
            messages.error(
                request, "This movie is not found in your wishlist.")
        else:
            Wishlist.objects.filter(
                user=selected_usr, movie=selected_movie).delete()
            messages.success(request, "Removed successfully.")
        # both wishlist view and movie detail view can remove movies from wishlist
        # redirect back to where it is come from
        if 'account' in previous_url:
            return HttpResponseRedirect(reverse('account:wishlist', args=(selected_usr.username,)))
        else:
            return HttpResponseRedirect(reverse('movie:movie_detail', args=(selected_movie.imdbID,)))
    else:
        raise Http404("User is not authorized.")


# add movies to the wishlist
def wishlist_add(request, user_name, movie_id):
    selected_usr = get_object_or_404(User, username=user_name)
    selected_movie = get_object_or_404(Movie, pk=movie_id)
    # authentication and make sure the movie is not in the wishlist already
    if request.user == selected_usr:
        if Wishlist.objects.filter(user=selected_usr, movie=selected_movie).exists():
            messages.error(request, "This movie is already in your wishlist.")
        else:
            record = Wishlist(user=selected_usr, movie=selected_movie)
            record.save()
            messages.success(request, "Added successfully.")
        return HttpResponseRedirect(reverse('movie:movie_detail', args=(movie_id,)))
    else:
        raise Http404("User is not authorized.")


# show user's blocklist
def banlist_request(request, user_name):
    selected_usr = get_object_or_404(User, username=user_name)
    if request.user.username != user_name:
        raise Http404("User is not authorized.")
    ban_list = selected_usr.banlist_owner.all()
    context = {
        "selected_usr": selected_usr,
        "users_in_banlist": ban_list,
    }
    return render(request, "account/banlist.html", context)


# add users to blocklist
def banlist_add(request, user_name, banned_user_name):
    banned_user = get_object_or_404(User, username=banned_user_name)
    previous_url = request.META.get('HTTP_REFERER')
    movie_id = previous_url.split('/')[4]
    if request.user.username == user_name:
        if BanList.objects.filter(user=request.user, blockedUser=banned_user).exists():
            messages.error(request, "This user is already in your blocklist.")
        else:
            record = BanList(user=request.user, blockedUser=banned_user)
            record.save()
            messages.success(request, "Added to your blocklist successfully.")
        return HttpResponseRedirect(reverse('movie:movie_detail', args=(movie_id,)))
    else:
        raise Http404("User is not authorized.")


# remove users in blocklist
def banlist_remove(request, user_name, banned_user_name):
    selected_usr = get_object_or_404(User, username=user_name)
    banned_user = get_object_or_404(User, username=banned_user_name)
    if request.user == selected_usr:
        if not BanList.objects.filter(user=request.user, blockedUser=banned_user).exists():
            messages.error(
                request, "This user is not found in your blocklist.")
        else:
            BanList.objects.filter(
                user=selected_usr, blockedUser=banned_user).delete()
            messages.success(request, "Unblock user successfully.")
        return HttpResponseRedirect(reverse('account:banlist', args=(user_name,)))
    else:
        raise Http404("User is not authorized.")


# register new accounts using Django user authentication system
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful.")
            if 'login' in request.get_full_path():
                return redirect('index', permanent=True)
            return redirect(request.GET.get('next', 'index'))
        else:
            return render(request=request, template_name="account/register.html",
                          context={"register_form": form})
    form = NewUserForm()
    return render(request=request, template_name="account/register.html",
                  context={"register_form": form})


# user accounts login
def login_request(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in. Redirect to homepage.")
        return redirect("index", permanent=True)
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if 'register' in request.get_full_path():
                    return redirect('index', permanent=True)
                return redirect(request.GET.get('next', 'index'))
            else:
                return render(request=request, template_name="account/login.html", context={"login_form": form})
        else:
            return render(request=request, template_name="account/login.html", context={"login_form": form})
    form = AuthenticationForm()
    return render(request=request, template_name="account/login.html", context={"login_form": form})


# user accounts logout, if does not logout mannual, its cookies will be kept for 2 weeks (default)
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index", permanent=True)


# user accounts password reset, for test purpose it will send the email in console
# for real email sending please change 'EMAIL_BACKEND' in the project settings
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "FilmFinder Password Reset Requested"
                    email_template_name = "account/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'filmfinder9900@gmail.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return HttpResponseRedirect(reverse('account:password_reset_done'))
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="account/password_reset.html", context={"password_reset_form": password_reset_form})
