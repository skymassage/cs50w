from django.contrib import admin
from .models import User, Listing, Bid, Comment, Category

class ListingAdmin(admin.ModelAdmin):
    # If there is only value, we should add a comma at the end.
    # Because ("watch_by") is a string not a tuple, but ("watch_by",) is a tuple containing a single string. 
    filter_horizontal = ("watch_by",) 

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)