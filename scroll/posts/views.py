import time

from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    return render(request, "posts/index.html")

# We want to detect that we're at the end of the page if we want to implement infinite scroll. 
# For example, if you're on a social media site, you don't want to have to load all posts at once, 
# you might want to load the first ten, and then when the user reaches the bottom, load the next ten.
def posts(request):

    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    data = []
    for i in range(start, end + 1):
        data.append(f"Post #{i}")

    time.sleep(1)   # Artificially delay speed of response

    # Use "JsonResponse" to return a JSON response. What we have here is a JSON object with a key called "posts". 
    # So we are creating our own API, which we can test out by visiting the url "<root_URL>/posts?start=<start_number>&end=<end_number>".
    # For example, the URL <root_URL>/posts?start=10&end=15 returns the following JSON:
    # {"posts": ["Post #10", "Post #11", "Post #12", "Post #13", "Post #14", "Post #15"]}
    return JsonResponse({
        "posts": data
    })