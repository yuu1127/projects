from django.urls import path, include, reverse_lazy
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

app_name = "account"

urlpatterns = [
    path('wishlist/<str:user_name>', views.wishlist_request, name="wishlist"),
    path('wishlist/<str:user_name>/rm_<int:movie_id>',
         views.wishlist_remove, name="wishlist_remove"),
    path('wishlist/<str:user_name>/add_<int:movie_id>',
         views.wishlist_add, name="wishlist_add"),
    path('blocklist/<str:user_name>', views.banlist_request, name="banlist"),
    path('blocklist/<str:user_name>/block_<str:banned_user_name>',
         views.banlist_add, name="banlist_add"),
    path('blocklist/<str:user_name>/unblock_<str:banned_user_name>',
         views.banlist_remove, name="banlist_remove"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html", success_url=reverse_lazy(
        'account:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html', success_url=reverse_lazy(
        'account:password_reset_complete')), name='password_change_request')
]
