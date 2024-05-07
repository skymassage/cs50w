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


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.all().order_by("-timestamp"),
        "comments": Comment.objects.all(),
        "form": PostForm()
    })


def comment(request, post_id):
    comments = Comment.objects.filter(post=Post.objects.get(pk=post_id)).order_by("-timestamp")
    return JsonResponse([comment.serialize() for comment in comments], safe=False) 


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


def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(poster=user).order_by("-timestamp")
    comments = [post.post_comments for post in posts]
    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts,
        "comments": comments,
    })


@login_required
def edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        new_content = data.get("content", "")
        post = Post.objects.get(pk=data.get("post_id", ""))
        post.content = new_content
        post.save()
        
        return JsonResponse({"content": new_content})

    return JsonResponse({"error": "POST request required."}, status=400) 
