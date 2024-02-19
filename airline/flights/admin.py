# In order to manipulate some of the underlying models in the admin app, 
# we need to import and register our models the models to the admin app. 
from django.contrib import admin
from .models import Flight, Airport, Passenger

# Register your models here.
admin.site.register(Flight)  # Tell Django's admin app that I would like to use the admin app to be able to manipulate "airports" and "flights".
admin.site.register(Airport)
admin.site.register(Passenger)

# You can log in at "/admin" to get Django's site administration interface to manipulate the underlying database ("airports" and "flights").
