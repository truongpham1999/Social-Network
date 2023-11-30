
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
    path("save_post/<int:post_id>", views.save_post, name="save_post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("get_comments/<int:post_id>", views.get_comments, name="get_comments"),
    path("add_comment/<int:post_id>", views.add_comment, name="add_comment"),
    path("search_users/", views.search_users, name="search_users"),
]
