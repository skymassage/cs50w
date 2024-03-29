# Remember that each time you change anything in auctions/models.py here, you need to first run "python3 manage.py makemigrations"
# and then "python3 manage.py migrate" to migrate those changes to your database.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max

# The User class inherits from "AbstractUser", so it will already have fields for a username, email, password, and you can add new fields to the User class.
class User(AbstractUser):
    pass

class Listing(models.Model):
    # null: If True, Django will store empty values as NULL in the database. A "Null" value represents the absence of data. 
    #       When a field has null=True, it means it is optional and can be left empty.
    #       Default is False which means the field must have a value in the database
    # blank: If True, the field can be left blank in forms. Default is False which means the field will be required
    
    # blank=True: Affects forms, allowing fields to be left blank. It is related to form validation and user input.
    # null=True: Affects the database, allowing fields to have a "null" value, i.e., no value. It is related to how data is stored in the database.
    # To summarize, null=True is about the database, and blank=True is about forms.
    
    # Best Practices: Use "null=True" for fields that represent optional data in the database. 
    #                 Use "blank=True" for fields that can be left empty in forms.

    # There are four cases:
    # 1) null=False, blank=False: 
    #    This is the default condition for modal fields. It means the value is required in both the database and the models.
    # 2) null=False, blank=True:
    #    This is contradictory. "null=False" means the field must have a value in the database, while "blank=True" means the field can be left blank in forms.
    #    This configuration means that you do not accept the value provided by the form for the field, but you can still have to provide a value for the field in some ways. 
    # 3) null=True, blank=False:
    #    It means the forms don't require a value, but the field does. This configuration is rarely used.
    # 4) null=True, blank=True:
    #    It means to allow NULL values in the database and also permit empty form submissions. This combination offers maximum flexibility.

    # Avoid using "null=True" on string-based fields such as CharField and TextField,
    # that means it has two possible values for "no data" (NULL), and the empty string (blank). In most cases, 
    # it's redundant to have two possible values for "no data"; the Django convention is to use the empty string, not NULL.
    # One exception is when a CharField has both "unique=True" and "blank=True" set. In this situation, 
    # "null=True" is required to avoid unique constraint violations when saving multiple objects with blank values.

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales_listings")
    name = models.CharField(max_length=100)     # "CharField" must use "max_length" to specify a maximum length,
    description = models.TextField()            # but "TextField" doesn't necessarily need "max_length".
    img = models.CharField(max_length=1000)      
    starting_price = models.DecimalField(max_digits=6, decimal_places=2) # "decimal_places" is the number of decimal places to store with the number.
                                                                         # "max_digits" is the maximum number of digits allowed in the number. 
                                                                         # Note that this number must be greater than or equal to "decimal_places".
    category = models.ForeignKey("Category", on_delete=models.SET_DEFAULT, blank=True, null=True, default="", related_name="category_listings")
    # If you need to create a relationship on a model that has not yet been defined, 
    # you can put the name of the model within "...", rather than the model object itself.
    # "SET_DEFAULT" means that when the ForeignKey is deleted, the object containing the ForeignKey will be set the default value.

    active = models.BooleanField(default=True)   
    watch_by = models.ManyToManyField(User, blank=True, related_name="watchlist") 
    # "null" has no effect on "ManyToManyField" since there is no way to require a relationship at the database level, so we don't set it.
    
    time = models.DateTimeField(auto_now_add=True) # "DateTimeField" automatically sets the field to now when the object is first created. N
                                                   # Note that the current date is always used; it's not just a default value that you can override.
    def __str__(self):
        return f"{self.name}"

    def bidder_num(self):
        return self.listing_bids.all().count()

    def current_price(self):
        # "aggregate" performs statistical calculations on a set of values ​​(such as a field of QuerySet) 
        # and returns the results in dictionary format. "aggregate" support the statistical calculations 
        # including AVG, COUNT, MAX, MIN, SUM, etc.
        # Note that the return of "aggregate" is a dict, and the key is "amount__max" here.
        bid_highest  = self.listing_bids.all().aggregate(Max("amount"))["amount__max"] 
        if self.bidder_num() > 0 and bid_highest > self.starting_price:
            return bid_highest
        else:
            return self.starting_price

    def winner(self):
        if self.bidder_num() > 0:
            return self.listing_bids.get(amount=self.current_price()).bidder
        else:
            return None 

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} bids ${self.amount} on {self.listing.name}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} comments on {self.listing}"

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name