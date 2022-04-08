from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializers import *
from .recommender import Recommender
from .MARSdb import Database
from rest_framework.renderers import JSONRenderer
import json

# Handles get and post requests from client, bridge between front end and backend
# When client makes a get request, return a list of genres for use in the genre dropdown list
# When client makes a post request, get the inputted user's anime list and return a list of recommendations
class SearchView(APIView):
    serializer_class = SearchSerializer

    def get(self, request):
        #print(request)
        returnString = "{\"genre_list\":["
        for item in Genre.objects.all():
            serializer = GenreSerializer(item)
            content = JSONRenderer().render(serializer.data).decode("utf-8")
            #print(content)
            returnString += content + ","
        returnString = returnString[:-1]
        returnString += "]}"
        return Response(returnString)

    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            selectedGenres = []
            if(serializer.data["selected_genres"]):
                selectedGenres = json.loads(serializer.data["selected_genres"])
            #Database.updateDB(1000)  #Adds/replaces first 1000 most popular shows on MAL.
            userList = Recommender.getList(serializer.data["userName"])
            # Below, we limit ourselves to 20 top entries, and 5 genres.
            # Selected genres is based off the client-side genre dropdown, and will overwrite generated genres
            recString = Recommender.recommend(userList, selectedGenres, 20, 5)

            return Response(recString)
