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
    # We can use request.GET["key_name"] or request.GET.get("key_name") to access the submitted data.
    # If the key doesn't exist, request.GET["key_name"] will return KeyError and request.GET.get("key_name") will return None.
    # Therefore, if you are not certain if the key exists, you can use request.GET.get("key_name").
    # Here it is better to use request.GET.get("key_name"), because we receive no value when submitting the placeholder "Select Category".
    # You still can use request.POST["key_name"], but you should use "try" and "except" statement to avoid the error.    
    category_name = request.GET.get("category_name")  
    if category_name == "others":
        return render(request, "auctions/index.html", {
            "title": "Category: Others",
            "category_name": "Others",
            "listings": Listing.objects.filter(category=None).filter(active=True),
            "categories": Category.objects.all().order_by("name")
        })

    elif category_name is None:
        return redirect("index")

    category = Category.objects.get(name=category_name)
    return render(request, "auctions/index.html", {
        "title": f"Category: {category_name}",
        "category_name": category_name,
        "listings": category.category_listings.filter(active=True),
        "categories": Category.objects.all().order_by("name")
    })


# "login_required(login_url=<URL_Name>): If the user isn't logged in, redirect to the URL with the <URL_Name> name. If the user is logged in, execute the view normally.
@login_required(login_url="login") # Add the "@login_required" decorator over the view function to ensure that only logged-in users can access the view.
def watchlist(request):
    user = request.user
    if request.method == "POST":
        # We are not sure which one of request.POST["watch_id"] and request.POST["remove_id"] can receive the value,
        # so it is better to use request.POST.get("key_name") here.
        if request.POST.get("watch_id"):
            watched_listing = Listing.objects.get(pk=request.POST["watch_id"]).watch_by.add(user)

        if request.POST.get("remove_id"):
            Listing.objects.get(pk=request.POST["remove_id"]).watch_by.remove(user)
    
    # Here we still need the GET method, because the logged in users can access the waatchlist page by clicking its buttonon the navigation bar.
    # So the following part shouldn't be moved to request.method == "POST".
    return render(request, "auctions/watchlist.html", {
        "listings": user.watchlist.all()   # You still can see the closed listing in the watchlist.
    }) 


@login_required(login_url="login") 
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

from django.db.models import Max

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_form": BidForm(),
        "comment_form": CommentForm(),
        "comments": listing.listing_comments.all()
    })


@login_required(login_url="login")
def comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        listing = Listing.objects.get(pk=listing_id)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.listing = listing
            form.save()
            return redirect("listing", listing_id=listing.id)
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid_form": BidForm(),
                "comment_form": form,
                "comments": listing.listing_comments.all()
            })


@login_required(login_url="login")
def bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)
        listing = Listing.objects.get(pk=request.POST["bid_listing_id"])
        if form.is_valid():
            form.instance.bidder = request.user
            form.instance.listing = listing
            if listing.listing_bids.all().count() == 0:
                if form.instance.amount >= listing.starting_price:
                    form.save()
                    return redirect("listing", listing_id=listing.id)
                else:
                    return render(request, "auctions/error.html", {
                        "message": "Your bid should not be lower than the starting price."
                    })
            else:
                if form.instance.amount > listing.current_price():
                    form.save()
                    return redirect("listing", listing_id=listing.id)
                else:
                    return render(request, "auctions/error.html", {
                        "message": "Your bid should be higher than the current bid."
                    })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid_form": form,
                "comment_form": CommentForm(),
                "comments": listing.listing_comments.all()
            })


@login_required(login_url="login")
def close(request):
    if request.method == "POST":
        listing_id = request.POST["close_listing_id"]
        Listing.objects.filter(pk=listing_id).update(active=False) 
        listing = Listing.objects.get(pk=listing_id)    
        return redirect("listing", listing_id=listing.id)

'''Method: .filer and .get
1. Return value
.get: An instance of a model class, called "instance" (also an object)
.filter: A collection object called "QuerySet". It can be used for iteration, but it's not a list.
         In the html template, we cannot use the QuerySet returned to obtain its attributes, 
         otherwise we will get None. We should use a for loop to obtain its attributes.


2. Error
.get: Only return a single search result (instance), so an error will occur if multiple results are found.
.filter: Return more than one search result (QuerySet), it returns None if not found (no results).


3. Make changes to tables with .save and .update 
.save: It can only be used with .get, .filter doesn't has the .save method.
       For example:
          user = User.objects.get(pk=user_id)
          user.username, user.email ="David", "david@example.com"
          user.save()
        
       .save can not only update existing records in the table, but also insert new records.
       For example:
           user = User(username="David", email="david@example.com")
           user.save()
           # Also, you can use .creata to insert a new record as below:
           User.objects.create(username="David", email="david@example.com")

.update: It can only be used with .filter, errors will occur if used with .get.
        .update can only be used to update existing object and can update multiple records at the same time.

         Note that it will be errors if use .update like this: 
            user = User.objects.filter(pk=user_id)
            user.update(username="David", email="david@example.com")
         You use .update like this :                                 
            User.objects.filter(pk=id).update(username="David", email="david@example.com")

.update is suitable for updating the existing records, and .save is suitable for inserting new records.
'''