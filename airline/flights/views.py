from django.shortcuts import render
from .models import Flight, Airport

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id) # In most cases, the "pk" (primary key) argument can also be replaced with "id", because id is the primary key in most cases.
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all()   # Note that "passengers" is the "related_name" argument which be used to track the passengers who happened to be on that flight.
    })


def book(request, flight_id):

    # For a post request, add a new flight
    if request.method == "POST":

        # Accessing the flight
        flight = Flight.objects.get(pk=flight_id)

        # Finding the passenger id from the submitted form data
        passenger_id = int(request.POST["passenger"])

        # Finding the passenger based on the id
        passenger = Passenger.objects.get(pk=passenger_id)

        # Add passenger to the flight
        passenger.flights.add(flight)

        # Redirect user to flight page
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))
