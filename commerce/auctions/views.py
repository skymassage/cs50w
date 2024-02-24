from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment, Category

from .models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password) # Use the included "objects.create_user" to create a user.
            user.save()                                                # Save the created user.
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# "login_required(login_url=<URL_Name>): If the user isn't logged in, redirect to the URL with the <URL_Name> name. If the user is logged in, execute the view normally.
@login_required(login_url="login") # Add the "@login_required" decorator over the view function to ensure that only logged-in users can access the view.
def create_listing(request):
    pass


@login_required(login_url="login")
def watchlist(request):
    pass



def listing(request, listing_id):
    pass
    
    return render (request, "auctions/listing.html", {

    })


def index(request):    
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "categories": Category.objects.all()
    })


def categorize(request):
    # request.GET.get("category_id")
    pass

def category(request, category_id):
    pass