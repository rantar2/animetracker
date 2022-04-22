from django.db import models
from django.contrib.postgres.fields import ArrayField
import base64
import json

# User Search model, contains all the information sent from the frontend to be read in the backend
class Search(models.Model):
    userName = models.CharField(max_length=16)
    selected_genres = models.CharField(max_length=8192)
    tv = models.BooleanField()
    movies = models.BooleanField()
    specials = models.BooleanField()
    ovas = models.BooleanField()
    onas = models.BooleanField()
    def _str_(self):
        return self.title


# AnimeEntry model, encapsulates all relevent information for a specific anime for storage in our database
class AnimeEntry(models.Model):
    name = models.CharField(max_length=120)  # for long titled anime
    MAL_ID = models.IntegerField()  # Numerical ID corresponding to anime in MAL DB
    rank = models.IntegerField()
    score = models.FloatField() # Average user score of show
    genres = models.ManyToManyField("Genre")
    main_picture = models.CharField(max_length=120)
    synopsis = models.CharField(max_length=8192)
    media_type = models.CharField(max_length=120)
    def _str_(self):
        return self.title

# Genre model, encapsulates all relevent information for a specific genre for storage in our database
class Genre(models.Model):
    genre_name = models.CharField(max_length=16)
    genre_id = models.IntegerField()
    def _str_(self):
        return "%s"%self.genre_name
