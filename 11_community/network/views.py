import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Comment
from .forms import PostForm
from django.http import JsonResponse
from django.core.paginator import Paginator

NUM = 10 # How many posts per page.

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

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


@login_required
def post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
                
        if form.is_valid:
            form.instance.poster = request.user
            form.save()
        else:
            return render(request, "network/index.html", {
                "posts": Post.objects.all(),
                "comments": Comment.objects.all(),
                "form": form
            })

    return redirect("index")


@login_required
def edit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        new_content = data.get("content", "")
        post = Post.objects.get(pk=int(data["post_id"]))
        post.content = new_content
        post.save()
        
        return JsonResponse({"content": new_content})

    return JsonResponse({"Error": "PUT request required."}, status=404) 


@login_required
def comment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        comment_content = data.get("comment_content", "")
        post = Post.objects.get(pk=int(data["post_id"]))
        comment = Comment(author=request.user, post=post, message=comment_content)
        comment.save()
        
        return JsonResponse({"Success": "Comment has been saved."}, status=201) 

    return JsonResponse({"Error": "POST request required."}, status=404) 


def show_comment(request, post_id):
    comments = Comment.objects.filter(post=Post.objects.get(pk=int(post_id))).order_by("-timestamp")
    return JsonResponse([comment.serialize() for comment in comments], safe=False) 


@login_required
def rate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post, user = Post.objects.get(pk=int(data["post_id"])), User.objects.get(pk=int(data["user_id"]))
        post.likes.add(user) if data["like"] else post.likes.remove(user)
        post.dislikes.add(user) if data["dislike"] else post.dislikes.remove(user)
        post.save()

        return JsonResponse({"Success": "Rates has been saved."}, status=204) 

    return JsonResponse({"Error": "POST request required."}, status=404)


def index(request):
    # Paginator(object_list, per_page): Under the hood, all methods of pagination use the Paginator class.
    # "object_list" is required and is a list, tuple, QuerySet, or other sliceable object with a count() or __len__() method. 
    # For consistent pagination, QuerySets should be ordered, e.g. with an order_by() clause or with a default ordering on the model.
    # "per_page" is required and is the maximum number of items to include on a page.

    # "<Paginator>.page_range" return a 1-based range iterator of page numbers.
    # "1-based" means 1-based numbering that is the computational idea of ​​indexing an ordered data structure by starting with 1 instead of 0.
    # "<Paginator>.get_page(<page_num>)" returns a Page object with the given 1-based index, while also handling out of range and invalid page numbers.
    # If <page_num> isn't a number, it will return the first page.
    # And if <page_num> is negative or greater than the number of pages, it returns the last page.
    
    # You usually won't construct <Page> objects by hand - you'll get them by iterating Paginator (<Paginator>.page_range), or by using <Paginator>.get_page().
    # "<Page>.number" returns the 1-based page number for <Page> (i.e. the current page number).
    # "<Page>.has_previous()" returns True if there's a previous page.
    # "<Page>.has_next()" returns True if there's a next page.
    # "<Page>.paginator" returns the associated Paginator object so as to use the method of the Paginator class.

    if request.GET.get("page") is None:
        page_number = int(1)
    else:
        page_number = request.GET.get("page")

    all_post = Post.objects.all().order_by("-timestamp")
    post_paginator = Paginator(all_post, NUM)                # Show 10 posts per page.
    post_page = post_paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "title": "All Posts",
        "posts_per_page": post_page,
        "form": PostForm(),
    })


def profile(request, username):
    if request.GET.get("page") is None:
        page_number = int(1)
    else:
        page_number = request.GET.get("page")

    user = User.objects.get(username=username)
    profile_posts = Post.objects.filter(poster=user).order_by("-timestamp")
    post_paginator = Paginator(profile_posts, NUM)
    post_page = post_paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "title": "My Profile" if user == request.user else f"{user.username}'s Profile",
        "profile": True,
        "user": user,
        "posts_per_page": post_page,
        "form": PostForm()
    })


def show_following(request):
    if request.GET.get("page") is None:
        page_number = int(1)
    else:
        page_number = request.GET.get("page")
    
    # "<QuerySet>.none()" creates a queryset (an instance of EmptyQuerySet) 
    # that never returns any objects and no query will be executed when accessing the results. 
    following_posts = Post.objects.none()
    for following_user in request.user.following.all():
        # Use '&' to take the intersection: <QuerySet1> & <QuerySet2>
        # Use '|' to take the union: <QuerySet1>| <QuerySet2>
        # User ".distinct()" to eliminate duplicate rows: (<QuerySet1> | <QuerySet2>).distinct()
        following_posts |= Post.objects.filter(poster=following_user) 
    following_posts = following_posts.order_by("-timestamp")
    
    post_paginator = Paginator(following_posts, NUM)
    post_page = post_paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "title": "My Following Posts",
        "posts_per_page": post_page,
        "following": True  # Setting "following" to True is to prevent the post form from being displayed.
    })


@login_required
def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        followed_user = User.objects.get(pk=int(data["user_id"]))
        if followed_user!= request.user:
            request.user.following.add(followed_user) if data["if_follow"] else request.user.following.remove(followed_user)
            request.user.save()
            return JsonResponse({"Success": "You have followed or unfollowed."}, status=204) 
            # Note that "204 No Content" doesn't return any content, so don't use "<response>.json()" for its response in JS.
        
        return JsonResponse({"Error": "You couldn't follow or unfollow yourself."}, status=404)

    return JsonResponse({"Error": "POST request required."}, status=404)