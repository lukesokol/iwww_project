from django.contrib import admin

from .models import Category, Photo, UserProfile

admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(UserProfile)