from django.db import models
import base64
import json

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)

    def _str_(self):
        return self.title

class Search(models.Model):
    userName = models.CharField(max_length=16)
    def _str_(self):
        return self.title

class AnimeEntry(models.Model):
    name = models.CharField(max_length=120)  # for long titled anime
    MAL_ID = models.IntegerField()  # Numerical ID corresponding to anime in MAL DB
    rank = models.IntegerField()
    genres = models.ManyToManyField("Genre")
    main_picture = models.CharField(max_length=120)
    synopsis = models.CharField(max_length=8192)
    def _str_(self):
        return self.title

class Genre(models.Model):
    genre_name = models.CharField(max_length=16)
    genre_id = models.IntegerField()
    def _str_(self):
        return "%s"%self.genre_name
