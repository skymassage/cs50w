# In order to manipulate some of the underlying models in the admin app, 
# we need to import and register our models the models to the admin app. 
# We can log in at "/admin" to get Django's site administration interface to manipulate the underlying database ("Airports", "Flight", "Passenger").
# We have created the superuser for this app, so go to "read_first.txt" in this project folder to see the superuser information for login in.
from django.contrib import admin
from .models import Flight, Airport, Passenger

# Another advantage of using the Django admin app is that we can customizable how to display the models in the admin interface.
class FlightAdmin(admin.ModelAdmin):
    # Here I can specify any particular settings that I want to apply to how the "Flight" admin page is displayed.
    # By default (i.e. I don't create this class) each item on the table looked like "<id> <origin> to <destination>".
    # I can say, in list_display, when you list all the flights and display them all to me, show me the id, origin, 
    # destination and duration.
    list_display = ("id", "origin", "destination", "duration")

# By default we just can see the available filghts when we're editing a passenger,
class PassengerAdmin(admin.ModelAdmin):
    # We can have a special way of manipulating "many to many" relationships inside of an attribute called "filter_horizontal".
    # And we will see both available and chosen flights so that we can manipulate theflight more conveniently.
    filter_horizontal = ("flights",)

# Register your models to tell Django's admin app that I would like to use the admin app to be able to manipulate "Airports" and "Flights", and "Passengers".
admin.site.register(Flight, FlightAdmin) # When I register "Flight", and in the second argument I can specify these particular settings when you view the admin interface.
admin.site.register(Airport)
admin.site.register(Passenger, PassengerAdmin)

# When we enter to the model Airports in the admin interface, because we don't customize it here, 
# each item on the table looks like "<city> (<code>)" which we have defined "__str__" for the class Airport in models.py.