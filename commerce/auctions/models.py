# Remember that each time you change anything in auctions/models.py here, you need to first run "python3 manage.py makemigrations"
# and then "python3 manage.py migrate" to migrate those changes to your database.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max

# The User class inherits from "AbstractUser", so it will already have fields for a username, email, password, and you can add new fields to the User class.
# The "User" class here conflicts with the "User" class that comes with Django.
# And we must add the line "AUTH_USER_MODEL = '<App_Name>.<lass_Name>'" to the setting.py file to tell Django we use the customized model class.
# So add this line "AUTH_USER_MODEL = 'auctions.User'" to our setting.py file.
class User(AbstractUser):
    pass

class Listing(models.Model):
    # null: If True, Django will store an empty value as NULL in the database. A "Null" value represents the absence of data. 
    #       Default is False which means the field must have a value (not include NULL) in the database
    # blank: blank determines whether the field will be required in forms.
    #        If True, the field can be left blank in forms. Default is False which means the field will be required
    # To summarize, null is about the database, and blank is about forms.
    
    # The exception is CharFields and TextFields, which in Django are never saved as NULL. 
    # Blank values in CharFields and TextFields are stored in the database as an empty string ('').
    # So avoid using "null=True" on string-based fields such as CharField and TextField,
    # that means it has two possible values for "no data" (NULL), and the empty string (blank). In most cases, 
    # it's redundant to have two possible values for "no data"; the Django convention is to use the empty string, not NULL.
    # One exception is when a CharField has both "unique=True" and "blank=True" set. In this situation, 
    # "null=True" is required to avoid unique constraint violations when saving multiple objects with blank values.
    
    # There are four cases:
    # 1) null=False, blank=False: 
    #    This is the default configuration and means that the value is required in both the database and the models.
    # 2) null=False, blank=True:
    #    This means that the form doesn't require a value but the database does.
    #    You don't accept the value provided by the form, but you can still have to provide a value for the database in some ways.
    #    a. The most common use is for optional string-based fields. 
    #       If NULL was also allowed you would end up with two different ways to indicate a missing value. 
    #       (If the field is also unique, you'll have to use null=True to prevent multiple empty strings from failing the uniqueness check.)
    #    b. Another common situation is that you want to calculate one field automatically based on the value of another.
    #    c. Another use is when you want to indicate that a ManyToManyField is optional. 
    #       Because this field is implemented as a separate table rather than a database column, null=True is meaningless. 
    #       The value of blank will still affect forms, though, controlling whether or not validation will succeed when there are no relations.
    # 3) null=True, blank=False:
    #    This means that the form requires a value but the database doesn't. This may be the most infrequently used configuration
    # 4) null=True, blank=True:
    #    It means to allow NULL values in the database and also permit empty form submissions. 
    #    This combination offers maximum flexibility, but this is not the recommended way to make string-based fields optional

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)     # "CharField" must use "max_length" to specify a maximum length,
    description = models.TextField()            # but "TextField" doesn't necessarily need "max_length".
    img = models.CharField(max_length=1000)      
    starting_price = models.DecimalField(max_digits=6, decimal_places=2) # "decimal_places" is the number of decimal places to store with the number.
                                                                         # "max_digits" is the maximum number of digits allowed in the number. 
                                                                         # Note that this number must be greater than or equal to "decimal_places".
    category = models.ForeignKey("Category", on_delete=models.SET_DEFAULT, blank=True, null=True, default="", related_name="category_listings")
    # If you need to create a relationship on a model that has not yet been defined, 
    # you can put the class name of the model within "...", rather than the model object itself.
    # That is, we haven't created the Category class yet, so put the Category inside of "".
    # "SET_DEFAULT" means that when the ForeignKey is deleted, the object containing the ForeignKey will be set the default value.

    active = models.BooleanField(default=True)   
    watch_by = models.ManyToManyField(User, blank=True, related_name="watchlist") 
    # "null" has no effect on "ManyToManyField" since there is no way to require a relationship at the database level, so we don't set it.
    
    time = models.DateTimeField(auto_now_add=True) # "DateTimeField" automatically sets the field to now when the object is first created.
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
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} bids ${self.amount} on {self.listing.name}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} comments on {self.listing}"

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name