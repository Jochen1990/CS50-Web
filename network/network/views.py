from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import datetime
import json
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
    return render(request, "network/index.html")


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
            follows = Follow.objects.create(
                user = user,
                followers = 0,
                following = 0 
            )
            follows.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def all_posts(request):
    posts = Post.objects.all().order_by('-timestamp')
    for post in posts:
        post.likes = Like.objects.filter(post=post.id).count()
        post.save() 
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    allLikes = Like.objects.all()
    whoYouLiked = []

    like_count = Like.objects.values('post').annotate(c=Count("post"))

    post_ids = list(Like.objects.values_list('post', flat=True))

    for post in posts:
        post.likes = Like.objects.filter(post=post.id).count()
        post.save()    

    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked = []
    
    if request.method == "POST":


        new_post = Post.objects.create(
            user = request.user,
            content = request.POST["post"],
            timestamp = datetime.datetime.now(),
            likes = 0
        )

        new_post.save()

        return HttpResponseRedirect(reverse(all_posts))

    else:
        return render(request, "network/all_posts.html", {
            'page_obj': page_obj,
            'whoYouLiked': whoYouLiked,
            'like_count' : like_count,
            'post_ids': post_ids
        })
    

def following(request):
    follow_ids = list(Follow_Users.objects.filter(user_id=request.user.id).all().values_list("user_following_id", flat = True))
    posts = Post.objects.filter(user__in = follow_ids).all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        pass

    else:
        return render(request, "network/following.html", {
            'page_obj': page_obj
        })

def profile(request, user_id):
    posts = Post.objects.filter(user=user_id).order_by('-timestamp').all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_user = list(dict.fromkeys(list(Post.objects.filter(user=user_id).values_list("user", flat=True))))[0]

    follower_num = Follow_Users.objects.values("user_following").annotate(freq=Count("user"))
    following_num = Follow_Users.objects.values("user").annotate(follows=Count("user"))


    follow_ids = list(Follow_Users.objects.values_list('user', flat=True))
    following_ids = list(Follow_Users.objects.values_list('user_following', flat=True))
    

    if request.method == "POST":
        follow_test = request.POST["follow-button"]
        if follow_test == 'Unfollow':
            print(Follow_Users.objects.filter(user=request.user.id, user_following=user_id))
            Follow_Users.objects.filter(user_following=user_id, user=request.user.id).delete()
        elif follow_test == 'Follow':
            follow = Follow_Users.objects.create(
                user = request.user,
                user_following = User.objects.get(id = user_id)
            )
            follow.save()
        pass
    
        follow_button_visibility = request.user.is_authenticated and request.user.id != user_id
        user_profile = Follow_Users.objects.filter(user=request.user.id).values_list("user_following", flat=True)
        if user_id in user_profile:
            follow_text = "Unfollow"
        else:
            follow_text = "Follow"

        return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

    else:  
        follow_button_visibility = request.user.is_authenticated and request.user.id != user_id
        user_profile = Follow_Users.objects.filter(user=request.user.id).values_list("user_following", flat=True)
        if user_id in user_profile:
            follow_text = "Unfollow"
        else:
            follow_text = "Follow"
        
        return render(request, "network/profile.html", {
            'page_obj': page_obj,
            'Follows': Follow.objects.filter(user=user_id).all(),
            'follow_button_visible': follow_button_visibility,
            'follow_text': follow_text,
            'follower_num': follower_num,
            'following_num': following_num,
            'posts_user': posts_user,
            'follow_ids': follow_ids,
            'following_ids': following_ids
        })


def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "successful", "data": data["content"]})

@csrf_exempt
def like(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        print(data.get("like"))
        if data.get("like"):
            Like.objects.create(user=request.user, post=post)
            post.likes = Like.objects.filter(post=post).count()
        else: 
            Like.objects.filter(user=request.user, post=post).delete()
            post.likes = Like.objects.filter(post=post).count()
        post.save()
        return HttpResponse(status=204)
    
    if request.method == "GET":
        return JsonResponse(post.serialize())