# In this file, we'll outline what data we want to store in our application. 
# Then, Django will determine the SQL syntax necessary to store information on each of our models.
from django.db import models

# Tell Django to update the database to include information about the models I just created. 
# In Django, we refer to this process as migrations. I create a migration to say, 
# here are some changes that I would like to apply to the database. 
# Then I migrate them to tell Django to take those changes and actually apply them to the database. 
# So it's a two-step process. First is to create the migration, which is instructions for how to actually manipulate the database. 
# Then take the migration step, which is to take those instructions and actually applying them to the underlying database.
# 1-step:
# To create a database from our models, we navigate to the main directory of our project and run the command: "python manage.py makemigrations"
# We wiil create a 0001_initial.py file in the "migrations" folder (flights/migrations/0001_initial.py). 
# We also will create a migration inside of 0001_initial.py where in this migration it's created a model called "flight." 
# This file has instructions to Django for how to manipulate the database to reflect the changes I have made to the model. 
# That is an instruction to Django to create a new model called "flight" that has these particular fields inside of it. 
# 2-step:
# If we want to apply the migration to Django's database, we can run "python manage.py migrate" to apply these migrations. 
# We'll see that some default migrations have been applied displayed in the terminal, 
# but notice one line that "Applying flights.0001_initial" means to apply that migration and create that table that is going to represent flights. 
# And we'll also notice that we now have a file called "db.sqlite3" in our project's directory.

'''
Create your models here.
class Flight(models.Model):
    origin = models.CharField(max_length=64) # The max length of this field doexn't exceed 64 characters.
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
'''

'''
Run these two commands "python3 manage.py makemigrations", "python3 manage.py migrate"
And we can run "python3 manage.py shell" to enter Django's shell where we can run Python commands within our project.
For example, we can run the following Python code in the terminal after entering Django's shell, and will see the following:
In [1]: from flights.models import Flight                                  # Import the flight model from model.py
In [2]: f = Flight(origin="New York", destination="London", duration=415)  # Create a new flight
In [3]: f.save()                                                           # Instert that flight into our database
In [4]: Flight.objects.all()                                               # Query for all flights stored in the database
Out[4]: <QuerySet [<Flight: Flight object (1)>]>                           # The output

The above output shows "Flight object (1)" that is not very informative.
We can fix that by defining a "__str__" function in the "Flight" class of  models.py:
def __str__(self):
    return f"{self.id}: {self.origin} to {self.destination}"

Leave Django's shell and enter shell again to run the following Python code:
In [1]: from flights.models import Flight              # Import our flight model again
In [2]: flights = Flight.objects.all()                 # Create a variable called flights to store the results of a query
In [3]: flights                                        # Displaying all flights
Out[3]: <QuerySet [<Flight: 1: New York to London>]>
In [4]: flight = flights.first()                       # Use "first()" to retrieve the first object from a queryset
In [5]: flight                                         # Printing flight information 
Out[5]: <Flight: 1: New York to London>
In [6]: flight.id                                      # Display flight id
Out[6]: 1
In [7]: flight.origin                                  # Display flight origin
Out[7]: 'New York'
In [8]: flight.destination                             # Display flight destination
Out[8]: 'London'
In [9]: flight.duration                                # Display flight duration
Out[9]: 415
In [10]: flight.delete()                                # Delete flight
Out[10]: (1, {'flights.Flight': 1})
'''


class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    # Specify the origin and destination fields as each Foreign Keys, which means they refer to another object.
    # By entering "Airport" as our first argument, we are specifying the type of object this field refers to.
    # "on_delete" gives instructions for what should happen if an airport is deleted. 
    # "on_delete=models.CASCADE" means that when an airport is deleted, all flights associated with it should also be deleted. 
    # "related name" is a way of accessing a relationship in the reverse order. For example, if we have an airport, 
    # and I want to know all of the flights that have that airport as their origin, the reasonable name for "related_name" can be "departures". 
    # So we can access all of the departures, which gets me all of the flights that are leaving from that airport. 
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

'''
Every time we make changes in models.py, we have to make migrations and then migrate. 
Note that you may have to delete your existing flight from New York to London, as it doesn't fit in with the new database structure.
So run these two commands again "python3 manage.py makemigrations", "python3 manage.py migrate".
Then enter the Django's shell (using "python3 manage.py shell"), and run the following code to see the following:
In [1]: from flights.models import *                                 # Import all models from model.py

In [2]: jfk = Airport(code="JFK", city="New York")                   # Create some new airports and save them to the database
In [3]: jfk.save()
In [4]: lhr = Airport(code="LHR", city="London")
In [5]: lhr.save()
In [6]: cdg = Airport(code="CDG", city="Paris")
In [7]: cdg.save()
In [8]: nrt = Airport(code="NRT", city="Tokyo")
In [9]: nrt.save()

In [10]: f = Flight(origin=jfk, destination=lhr, duration=414)       # Add a flight and save it to the database
In [11]: f.save()

In [12]: f                                                           # Display some info about the flight
Out[12]: <Flight: 1: New York (JFK) to London (LHR)>
In [13]: f.origin
Out[13]: <Airport: New York (JFK)>

In [14]: lhr.arrivals.all()                                          # Using "related_name" to query by airport of arrival
Out[14]: <QuerySet [<Flight: 1: New York (JFK) to London (LHR)>]>

In [15]: Airport.objects.all()                                       # It gets me all of the airports using "all()"
Out[15]: <QuerySet [<Airport: New York (JFK)>, <Airport: London (LHR)>, <Airport: Paris (CDG)>, <Airport: Tokyo (NRT)>]>

In [16]: Airport.objects.filter(city="New York")                     # Use "filter()" to find all airports based in New York
Out[16]: <QuerySet [<Airport: New York (JFK)>]>

In [17]: Airport.objects.filter(city="New York").first()             # Get me the first and only thing in that "QuerySet"
Out[17]: <Airport: New York (JFK)>

In [18]: Airport.objects.get(city="New York")                        # If you know you're only going to get one result back, you can use "get()" to get only one airport in New York. But it will throw an error if there's more than one result, or if there's none.
Out[18]: <Airport: New York (JFK)>

In [6]: jfk = Airport.objects.get(city="New York")                   # Assigning some airports to variable names:
In [7]: cdg = Airport.objects.get(city="Paris")
In [8]: f = Flight(origin=jfk, destination=cdg, duration=435)        # Creating and saving a new flight:
In [9]: f.save()
''' 

class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    # Passengers have a Many to Many relationship with flights, because a passenger may take different flights, 
    # and a flight may have multiple passengers. So we describe in Django using "ManyToManyField".
    # The first argument in this field is the class of objects that this one is related to.
    # So every passenger could be associated with many flights. Note the this is the "Passenger" class.
    # "blank=True"  means a passenger can have no flights
    # related_name="passengers" will allow us to find all passengers on a given flight.
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers") 
    

    def __str__(self):
        return f"{self.first} {self.last}"