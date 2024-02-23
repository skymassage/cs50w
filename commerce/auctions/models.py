# Remember that each time you change anything in auctions/models.py here, you need to first run "python3 manage.py makemigrations"
# and then "python3 manage.py migrate" to migrate those changes to your database.
from django.contrib.auth.models import AbstractUser
from django.db import models

# The User class inherits from "AbstractUser", so it will already have fields for a username, email, password, and you can add new fields to the User class.
class User(AbstractUser):
    pass


# class Listing(models.Model):


# class Bid(models.Model):


# class Comments(models.Model):


# Also need to add additional models to represent details about auction listings, bids, comments, and auction categories. 
