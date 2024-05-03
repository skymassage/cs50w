from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
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