# Any of the views you write may use these three functions to interact with encyclopedia entries.
import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Return a list of the names of all encyclopedia entries currently saved. 
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Save an encyclopedia entry, given its title and Markdown content. 
    If an existing entry with the same title already exists, it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieve an encyclopedia entry by its title.
    And return its Markdown contents if the entry exists, or None if the entry does not exist.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def search_entry(query):
    results = []
    for entry in list_entries():
        # "findall(pattern, string, flags)" returns a subset of characters that a specified "pattern" matches a given "string".
        # "flags=re.IGNORECASE" search modifier forces the function to which is applied to perform a case-insensitive search.
        if re.findall(query, entry, re.IGNORECASE):
            results.append(entry)
    return results 