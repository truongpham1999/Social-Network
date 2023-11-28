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

    if request.user.is_authenticated:
        for post in posts:
            post.is_liked = post.is_like_by_user(request.user)
    else:
        for post in posts:
            post.is_liked = False

    # using the paginate_posts function to paginate posts
    posts, previous_page, next_page = paginate_posts(posts, request.GET.get('page'), 2)

    return render(request, "network/index.html", {
        "posts": posts,
        "previous_page": previous_page,
        "next_page": next_page,
    })

def add_comment(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        content = data.get('content')
        post = Post.objects.get(pk=post_id)
        if content:
            comment = Comment(content=content, commenter=request.user, post=post)
            comment.save()
            return JsonResponse({'success': True})
        return JsonResponse({'error': 'Comment content is empty'}, status=400)

def get_comments(request, post_id):
    if request.method == 'GET':
        post = Post.objects.get(pk=post_id)
        comments = post.comments.all().order_by('-date')
        return JsonResponse([comment.serialize() for comment in comments], safe=False)

@csrf_exempt
def like(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)

        # check if the like already exists
        is_liked = Like.objects.filter(post=post, liker=request.user).exists()

        if data.get('like'):
            if not is_liked:
                like = Like(post=post, liker=request.user)
                like.save()
                return JsonResponse({'success': True, 'like': True})
        else:
            if is_liked:
                Like.objects.filter(post=post, liker=request.user).delete()
                return JsonResponse({'success': True, 'like': False})

    return JsonResponse({'success': False})

@csrf_exempt
def save_post(request, post_id):
    if request.method == 'PUT' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            post = Post.objects.get(pk=post_id)
            post.content = data.get('newText')
            post.save()
            return JsonResponse({'success': True})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': "Invalid request method"}, status=400)

def following_page(request):
    if request.user.is_authenticated:
        # Get the users that the logged-in user is following
        followed_users = User.objects.filter(followed__follower=request.user)
        posts = Post.objects.filter(poster__in=followed_users).order_by('-date')
        
        # using the paginate_posts function to paginate posts
        posts, previous_page, next_page = paginate_posts(posts, request.GET.get('page'), 2)

        return render(request, "network/following.html", {
            "posts": posts,
            "previous_page": previous_page,
            "next_page": next_page,
        })
    else:
        return HttpResponseRedirect(reverse("login"))

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
            if follow:
                follow.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Follow object does not exist'}, status=400)
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
    followers_count = profile_user.followed.count()
    following_count = profile_user.followers.count()

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
        "followers_count": followers_count,
        "following_count": following_count,
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
