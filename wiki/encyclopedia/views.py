from markdown2 import markdown
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def enter(request, title):
    title = title.strip() # Remove the leading and trailing spaces of "title".
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/entry.html", {
            "error": True,
            "entry_title": "404 Error",
            "content": f"<h1>404 Error: Entry for \"{title}\" not found</h1>"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "error": False,
            "entry_title": title,  # URLs cannot contain spaces. URL encoding normally replaces a space with a plus (+) sign or with "%20".
                                   # So here the space in "" of the url will be replaced by "%20".
            "content": markdown(content, safe_mode=True) # "safe_mode=True" means to ensure that the converted HTML is safe.
        })


def search(request):
    query = request.GET.get('q').strip()
    if query in util.list_entries():
        return redirect("wiki:entry", title=query)  # here the space in "query" of the url will be replaced by "+".

    results = util.search_entry(query)
    if not results:      # Check if "results" is empty.
        return render(request, "encyclopedia/search.html", {
            "no_results": True
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "no_results": False,
            "query": query,
            "entries": results
        })
 

def random_page(request): # Don't use "random" for the function name, because we are using the "random" package.
    # "HttpResponseRedirect" only supports hard-coded urls, that's why we need "reverse".
    # You can use "args" in "reverse" to pass the parameters for urls.
    return HttpResponseRedirect(reverse("wiki:entry", args=[random.choice(util.list_entries())]))
    
    # We can also use the "redirect" function, there are two way to use it.
    # Pass the name of a view and optionally some positional or keyword arguments, 
    # and the URL will be reverse resolved using "reverse()":
    # return redirect("wiki:entry", title=random.choice(util.list_entries())) 
    # Pass a hardcoded url to "redirect":
    # return redirect(reverse("wiki:entry", args=[random.choice(util.list_entries())])) 

def edit(request, title):
    return render(request, "encyclopedia/edit.html")

def create(request):
    
    return render(request, "encyclopedia/create.html")