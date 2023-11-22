from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Follow, Like, Comment

def paginate_posts(posts, page_number, posts_per_page):
    # Pagination, show 2 posts per page
    paginator = Paginator(posts, posts_per_page)

    # Get the current page number from the request's GET parameter
    page = page_number

    try:
        # Get the Page object for the requested page
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page of results
        posts = paginator.page(paginator.num.pages)

    # Calculate previous and next page numbers
    previous_page = posts.previous_page_number() if posts.has_previous() else None
    next_page = posts.next_page_number() if posts.has_next() else None

    return posts, previous_page, next_page


def index(request):
    posts = Post.objects.all().order_by('-date')

    # using the paginate_posts function to paginate posts
    posts, previous_page, next_page = paginate_posts(posts, request.GET.get('page'), 2)

    return render(request, "network/index.html", {
        "posts": posts,
        "previous_page": previous_page,
        "next_page": next_page,
    })

@csrf_exempt
def follow_unfollow(request, profile_user_id):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        profile_user = User.objects.get(pk=profile_user_id)

        if data.get('follow'):
            follow = Follow(follower=request.user, followed=profile_user)
            follow.save()
            return JsonResponse({'success': True})
        else:
            follow = Follow.objects.get(follower=request.user, followed=profile_user)
            follow.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def new_post(request):
    if request.method == "POST":
        content = request.POST["new_post"]
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, poster=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    posts = profile_user.posts.all().order_by('-date')

    # using the paginate_posts function to paginate posts
    posts, previous_page, next_page = paginate_posts(posts, request.GET.get('page'), 2)

    # check if the logged-in user is following the profile user
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, followed=profile_user).exists()

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "previous_page": previous_page,
        "next_page": next_page,
        "is_following": is_following,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
