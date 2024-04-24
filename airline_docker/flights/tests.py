# Instead of running "python3 <current_directory>/tests.py", run "python3 manage.py test flights" to see the testing results.
# It will create a database for testing and destroy it at the end, so it wouldn't change our app's database.
from django.test import Client, TestCase
from django.db.models import Max
from .models import Flight, Airport, Passenger

# One advantage to using the "TestCase" library is that when we run our tests, 
# an new seperate database will be created for testing purposes only.
# This is helpful because we avoid the risk of accidentally modifying or deleting existing entries in our databse 
# and we don't have to worry about removing dummy entries that we created only for testing.
# So we'll create a new class that extends the "TestCase" class we just imported. 
class FlightTestCase(TestCase):  
    # Within this class, we define a "setUp" function (the function name must be "setUp") to do some initial setup 
    # in order to make sure that there's some data that we can work with and test with.
    def setUp(self):
        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        # If the first and second parameters of "assertEqual" are the same, return true, otherwise return false.
        # The third argument is optional which is the failing message when the test fails.
        self.assertEqual(a.departures.count(), 3) # Make sure our departures fields work correctly by attempting to count 
                                                  # the number of departures (which we know should be 3) from airport "AAA".

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())

    # we may not only check that specific features are working properly, but also that individual web pages load as expected.
    # When creating web applications, we will probably want to check not just whether or not specific functions work, 
    # but also whether or not individual web pages load as intended. 
    # We can do this by creating a "Client" object in our Django testing class, and then making requests using that object.
    def test_index(self): # Makes sure that we get a response code of 200 and that all of our flights are added to the context of a response.
        c = Client() # To use the test client, instantiate "django.test.Client"
        response = c.get("/flights/") # Use "<client>.get" ot make a GET request on the provided path and returns a Response object.
        self.assertEqual(response.status_code, 200) # Access the HTTP status code of the Response object by "<response>.status_code".
        self.assertEqual(response.context["flights"].count(), 3) # Use "<response>.context["key"]"" to access the values 
                                                                 # that used as the placeholder to render the template.
                                                                 # Note that we sent the GET request to the "/flights/" route 
                                                                 # whose view is the "index" function 
                                                                 # that passes "flights": Flight.objects.all() to the template for rendering.

        # The test client is a Python class that acts as a dummy web browser, 
        # allowing you to test your views and interact with your Django-powered application programmatically. There are some features:
        # 1. The test client can simulate GET and POST requests on a URL and observe the response, 
        #    everything from low-level HTTP (result headers and status codes) to page content.
        # 2. The test client can test that a given request is rendered by a given Django template, 
        #    with a template context that contains certain values.
        # 3. The test client does not require the web server to be running, 
        #    because it avoids the overhead of HTTP and deals directly with the Django framework. 
        # When retrieving pages, remember to specify the path of the URL, not the whole domain. 
        # For example, this is correct: <client>.get("/login/")
        # This is incorrect: <client>.get("https://www.example.com/login/")
        # The test client is not capable of retrieving web pages that are not powered by your Django project.

        # "<response>.get" returns a Response object which is not the same as the HttpResponse object returned by Django views; 
        # the test response object has some additional data useful for test code to verify. A Response object has the following attributes:
        # content: 
        #   The body of the response, as a bytestring. This is the final page content as rendered by the view, or any error message.
        # context: 
        #   The template Context instance that was used to render the template that produced the response content.
        #   If the rendered page used multiple templates, then context will be a list of Context objects, in the order in which they were rendered.
        #   Regardless of the number of templates used during rendering, you can retrieve context values using "[]".

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
