
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.new_post, name="newPost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow_unfollow/<int:profile_user_id>", views.follow_unfollow, name="follow_unfollow"),
    path("following_page", views.following_page, name="following_page"),
]
