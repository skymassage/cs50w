from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Flight, Airport, Passenger

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id) # In most cases, the "pk" (primary key) argument can also be replaced with "id", because id is the primary key in most cases.
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),  # Note that "passengers" is the "related_name" argument which be used to track the passengers who happened to be on that flight.
        "non_passengers": Passenger.objects.exclude(flights=flight).all()   # Use "exclude()" to exclude certain objects from a query. 
                                                                            # Here is to exclude the passenger objects which have corresponded to this flight object,
                                                                            # i.e., exclude the passengers who are already on this flight.
    })


def book(request, flight_id):
    if request.method == "POST":
        # There is definitely some error checking that we should be doing here. 
        # But for simplicity, let's just assume for now that we're able to get a flight and get a passenger.
        flight = Flight.objects.get(pk=flight_id)           # Accessing the flight.
        passenger_id = int(request.POST["passenger"])       # Finding the passenger id from the submitted form data.
        passenger = Passenger.objects.get(pk=passenger_id)  # Finding the passenger based on the id.
        passenger.flights.add(flight)                       # Add passenger to the flight using "add()",
                                                            # i.e., make this passenger object correspond to this flight oject.

        # return HttpResponseRedirect(reverse("flight:flight", args=[flight.id]))
        return redirect("flight:flight", flight_id=flight.id) 
