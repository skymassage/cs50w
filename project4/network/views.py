'''
CSRF token validation settings in Django are divided into global and local settings:

Global: Set the "django.middleware.csrf.CsrfViewMiddleware" middleware in "setting.py".
        Django performs CSRF token validation on all POST requests by default.
        If the validation fails, a 403 error will occur.
        Therefore, {% csrf_token %} needs to be added to <form>.
        Commenting "django.middleware.csrf.CsrfViewMiddleware" can remove all CSRF token verification, 
        but it will make our website completely unable to prevent CSRF attacks.

Local: Set CSRF token validation by setting the "@csrf_protect" decorator for the current view function, 
       even if "django.middleware.csrf.CsrfViewMiddleware" is not set in settings.
       Note adding {% csrf_token %} in HTML.
       Besides, "@csrf_exempt" cancels the CSRF token validation of the current view function, 
       even if "django.middleware.csrf.CsrfViewMiddleware" is set in settings.
'''

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
        
        print(request.headers)
        
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
        post = Post.objects.get(pk=data["post_id"])
        post.content = new_content
        post.save()
        
        return JsonResponse({"content": new_content})

    return JsonResponse({"error": "PUT request required."}, status=404) 


@login_required
def comment(request):
    if request.method == "POST":
        data = json.loads(request.body)

        comment_content = data.get("comment_content", "")
        post = Post.objects.get(pk=data["post_id"])        
        comment = Comment(author=request.user, post=post, message=comment_content)
        comment.save()
        
        return JsonResponse({"Sucess": "Comment has been saved."}, status=201) 

    return JsonResponse({"Error": "POST request required."}, status=404) 


def show_comment(request, post_id):
    comments = Comment.objects.filter(post=Post.objects.get(pk=post_id)).order_by("-timestamp")
    return JsonResponse([comment.serialize() for comment in comments], safe=False) 


@login_required
def rate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post, user = Post.objects.get(pk=data["post_id"]), User.objects.get(pk=data["user_id"])
        post.likes.add(user) if data["like"] else post.likes.remove(user)
        post.dislikes.add(user) if data["dislike"] else post.dislikes.remove(user)
        post.save()

        return JsonResponse({"Sucess": "Rates has been saved."}, status=204) 

    return JsonResponse({"error": "POST request required."}, status=404)

def follow(request):
    if request.method == "POST":

        return JsonResponse({"Sucess": "You have followed."}, status=204) 

    return JsonResponse({"error": "POST request required."}, status=404)

def show_following(request):
    return

def index(request):
    # Paginator(object_list, per_page): Under the hood, all methods of pagination use the Paginator class.
    # "object_list" is required and is a list, tuple, QuerySet, or other sliceable object with a count() or __len__() method. 
    # For consistent pagination, QuerySets should be ordered, e.g. with an order_by() clause or with a default ordering on the model.
    # "per_page" is required and is the maximum number of items to include on a page.

    # "<Paginator>.page_range" return a 1-based range iterator of page numbers.
    # "1-based" means 1-based numbering that is the computational idea of ​​indexing an ordered data structure by starting with 1 instead of 0.
    # "<Paginator>.get_page(<page_num>)" returns a Page object with the given 1-based index, while also handling out of range and invalid page numbers.
    # <page_num> isn't a number, it returns the first page. And <page_num> is negative or greater than the number of pages, it returns the last page.
    
    # You usually won't construct Page objects by hand - you'll get them by iterating Paginator (<Paginator>.page_range), or by using <Paginator>.get_page().
    # "<Page>.number" returns the 1-based page number for <Page> (i.e. the current page number).
    # "<Page>.has_previous()" returns True if there's a previous page.
    # "<Page>.has_next()" returns True if there's a next page.
    # "<Page>.paginator" returns the associated Paginator object so as to use the method of the Paginator class.

    if request.GET.get("page") is None:
        page_number = int(1)
    else:
        page_number = request.GET.get("page")

    all_post = Post.objects.all().order_by("-timestamp")
    post_paginator = Paginator(all_post, 10)                # Show 10 posts per page.
    post_objs = post_paginator.get_page(page_number)

    # "<QuerySet>.none()" creates a queryset (an instance of EmptyQuerySet) 
    # that never returns any objects and no query will be executed when accessing the results. 
    comment_objs = Comment.objects.none()
    for post in post_objs:
        # Use '&' to take the intersection: <QuerySet1> & <QuerySet2>
        # Use '|' to take the union: <QuerySet1>| <QuerySet2>
        # User ".distinct()" to eliminate duplicate rows: (<QuerySet1> | <QuerySet2>).distinct()
        comment_objs |= Comment.objects.filter(post=post)

    return render(request, "network/index.html", {
        "posts_per_page": post_objs,
        "comments": comment_objs,
        "form": PostForm()
    })


def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(poster=user).order_by("-timestamp")
    comments = [post.post_comments for post in posts]
    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts,
        "comments": comments,
    })