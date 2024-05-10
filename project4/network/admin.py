from django.contrib import admin
from .models import User, Post, Comment

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("following", "followers")

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("likes", "dislikes") 

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(User, UserAdmin)
