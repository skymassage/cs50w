'''
QuerySet refers to a collection for database query. 
QuerySet is a suitable choice when you need to obtain a set of data that meets certain conditions from the database, 
or when you need to perform database query operations (such as filtering, ordering, etc.). For example:

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
all_books = Book.objects.all()  # Query all books
specific_author_books = Book.objects.filter(author="J.K. Rowling") # Query books whose author is a specific value
other_authors_books = Book.objects.exclude(title="Harry Potter")   # Exclude books whose title is a specific value
sorted_books = Book.objects.order_by(author="J.K. Rowling")        # Sort books alphabetically by author
specific_book = Book.objects.get(title="Harry Potter")             # Get a single book that meets the conditions
'''

'''
Instance refers to a single object of a specific database model. 
In other words, an instance of the model corresponds to a row of table in the database. 
By creating instances of model classes, you can manipulate and access data in database. 
Use instance when you need to perform CRUD (Create, Read, Update, Delete) operations on a single row in the database.
For example:

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
book_instance = Book.objects.create(title="Harry Potter", author="J.K. Rowling") # Create a Book instance
single_book = Book.objects.get(title="Harry Potter")                             # Get a single instance
'''

'''
QuerySet is used to perform database query operations and return a collection of data, 
while instance is used to operate on a single database record. 
Depending on the requirements, one or a combination of both can be used.
'''
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


# "login_required(login_url=<URL_Name>): If the user isn't logged in, redirect to the URL with the <URL_Name> name. If the user is logged in, execute the view normally.
@login_required(login_url="login") # Add the "@login_required" decorator over the view function to ensure that only logged-in users can access the view.
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            form.instance.seller = request.user  # Use "instance" to set the "seller" field value.
            new_listing = form.save()            # Save a new created object from form and assign it to a variable.
            return redirect("listing", listing_id=new_listing.pk)
        else:
            return render(request, "auctions/creat.html", {
                "form": form
            })

    return render(request, "auctions/creat.html", {
        "form": ListingForm(),
    })


def listing(request, listing_id):
    
    return render (request, "auctions/listing.html", {
        "title": Listing.objects.get(pk=listing_id)
    })

