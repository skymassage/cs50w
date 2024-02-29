from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ListingForm, BidForm, CommentForm
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




def index(request):    
    return render(request, "auctions/index.html", {
        "title": "All Listings",
        "category_name": "All Listings",
        "listings": Listing.objects.filter(active=True),
        "categories": Category.objects.all().order_by("name")  # Use "order_by" to sort QuerySets based on field names (attributes).
    })


def category(request):
    category_name = request.GET["category_name"]
    if category_name == "others":
        return render(request, "auctions/index.html", {
            "title": "Category: Others",
            "category_name": "Others",
            "listings": Listing.objects.filter(category=None).filter(active=True),
            "categories": Category.objects.all().order_by("name")
        })

    category = Category.objects.get(name=category_name)
    return render(request, "auctions/index.html", {
        "title": f"Category: {category_name}",
        "category_name": category_name,
        "listings": category.category_listings.filter(active=True),
        "categories": Category.objects.all().order_by("name")
    })


@login_required(login_url="login")
def watchlist(request):
    user = request.user
    if request.method == "POST":
        # We can use request.POST["key_name"] or request.POST.get("key_name") to access the submitted data.
        # But it is better to use request.POST.get("key_name") here. 
        # If the key doesn't exist, request.POST["key_name"] will return KeyError and request.POST.get("key_name") will return None.
        # So if you are not certain if the key exists, you can use request.POST.get("key_name").
        # Here you still can use request.POST["key_name"], but you should use "try" and "except" statement to avoid the error.
        if request.POST.get("watch_id"):
            watched_listing = Listing.objects.get(pk=request.POST["watch_id"]).watch_by.add(user)

        if request.POST.get("discard_id"):
            Listing.objects.get(pk=request.POST["discard_id"]).watch_by.remove(user)

    return render(request, "auctions/watchlist.html", {
        "listings": user.watchlist.all()
    }) 



def listing(request, listing_id):
    
    return render (request, "auctions/listing.html", {
        "title": Listing.objects.get(pk=listing_id)
    })


# "login_required(login_url=<URL_Name>): If the user isn't logged in, redirect to the URL with the <URL_Name> name. If the user is logged in, execute the view normally.
@login_required(login_url="login") # Add the "@login_required" decorator over the view function to ensure that only logged-in users can access the view.
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid:
            
            return redirect("listing", )
        
        else:
            return render(request, "auctions/creat.html", {
                "form": form
            })

    # print(ListingForm())
    return render(request, "auctions/creat.html", {
        "form": ListingForm(),
        "categories": Category.objects.all().order_by("name")
    })