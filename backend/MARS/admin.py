from django.contrib import admin
from .models import User

class MARSAdmin(admin.ModelAdmin):
    list_display = ("username", "password")

# Register your models here.
admin.site.register(User, MARSAdmin)