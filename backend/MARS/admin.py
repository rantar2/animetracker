from django.contrib import admin
from .models import Search, AnimeEntry, Genre

class MARSAdmin(admin.ModelAdmin):
    list_display = ("username", "password")

# Register your models here.
#admin.site.register(User, MARSAdmin)
admin.site.register(Search)
admin.site.register(AnimeEntry)
admin.site.register(Genre)
