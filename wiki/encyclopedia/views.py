from django.shortcuts import render

# Create your views here.
from markdown2 import markdown
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import random
from . import util
from .forms import EntryForm  # Separate the forms into another .py file. Import module from the file of the same directory by ".<file_name>".


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def enter(request, title):
    # Because "title" is from urls, if "title" contain blank space characters in the URL, they will be replaced "%20".
    # But when "title" is passed to the view functiotn, "%20" will be converted back into blank space characters.
    title = title.strip() # Remove the leading and trailing spaces of "title".
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "error_title": "No Entry Found",
            "error_message": f"404 Error: Entry for \"{title}\" not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_title": title, # URLs cannot contain spaces. URL encoding normally replaces a space with a plus ('+') sign or with a "%20".
                                  # Here spaces in "title" of the url will be replaced by "%20" when rendering the template.
            "content": markdown(content, safe_mode=True) # "markdown()" converts Markdown syntax into HTML.
                                                         # If you are using Markdown on a web system which will transform text provided by untrusted users, 
                                                         # "safe_mode=True" ensures that the user's HTML tags are either replaced, removed or escaped.
        })


def search(request):
    query = request.GET.get("q").strip()
    if query in util.list_entries():
        return redirect("wiki:entry", title=query)  # Here the space in "query" of the url will be replaced by "+".

    results = util.search_entry(query)
    if not results:      # Check if "results" is empty.
        return render(request, "encyclopedia/error.html", {
            "error_title": "No Results",
            "error_message": "No results were found. You can create a new entry for it."
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "entries": results
        })

def random_page(request): # Don't use "random" as the function (view) name, because we are using the "random" package.
    # "HttpResponseRedirect" only supports hard-coded urls, that's why we need "reverse".
    # You can use "args" in "reverse" to pass the parameters for urls.
    return HttpResponseRedirect(reverse("wiki:entry", args=[random.choice(util.list_entries())])) # Note that use "[]" for agrs.
    
    # We can also use the "redirect" function, there are two way to use it.
    # Pass the name of a view and optionally some positional or keyword arguments:
    # return redirect("wiki:entry", title=random.choice(util.list_entries())) 
    # Pass a hardcoded url to "redirect":
    # return redirect(reverse("wiki:entry", args=[random.choice(util.list_entries())])) 


def create(request):
    if request.method == "POST":
        create_form = EntryForm(request.POST)
        if create_form.is_valid():
            title = create_form.cleaned_data.get("title").strip()
            content = create_form.cleaned_data.get("content").strip()
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "error_title": "Entry Creation Failed",
                    "error_message": "Entry already exists. Entry titles cannot be repeated."
                })

            util.save_entry(title, content)
            return redirect("wiki:entry", title=title)

        else:
            return render(request,  "encyclopedia/create.html", {
                "create_form": create_form
            })
    
    # print(EntryForm())  # You can print "EntryForm()" to see exactly what it is.
    return render(request, "encyclopedia/create.html", {
        "create_form": EntryForm()
    })


def edit(request, title):
    if request.method == "POST":
        if request.POST.get("delete"):
            filename = f"entries/{title}.md"
            default_storage.delete(filename)
            return redirect("wiki:index")

        edit_form = EntryForm(request.POST)
        if edit_form.is_valid():
            title = edit_form.cleaned_data.get("title").strip()
            content = edit_form.cleaned_data.get("content").strip()
            util.save_entry(title, content)
            return redirect("wiki:entry", title=title)
        else:
            return render(request, "encyclopedia/edit.html", {
                "edit_form": edit_form
            })
          
    return render(request, "encyclopedia/edit.html", {
        # Set initial values for the required fields by giving an initial data dictionary to "EntryForm".
        # Note that it should be a dictionary that maps the names of fields to their respective initial values. 
        "edit_form": EntryForm({"title": title, "content": util.get_entry(title)})
    })