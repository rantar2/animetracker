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

max_results = 20
max_genres = 5
default_list = ['Drama']
class SearchView(APIView):
    serializer_class = SearchSerializer

    def get(self, request):
        returnString = "{\"genre_list\":["
        for item in Genre.objects.all():
            serializer = GenreSerializer(item)
            content = JSONRenderer().render(serializer.data).decode("utf-8")
            returnString += content + ","
        returnString = returnString[:-1]
        returnString += "]}"
        return Response(returnString)

    def post(self, request):
        """Call up backend reccomender with parameters provided by user"""
        #Database.updateDB(5000)
        max_results = request.data["max_results"]
        if max_results <= 0:
            max_results = 20

        mediaTypes = [request.data["tv"], request.data["movies"], request.data["specials"], request.data["ovas"], request.data["onas"]]
        print(mediaTypes)

        # If user provides no username (for non MAL users or otherwise)
        if request.data["userName"] == "":
            # If nothing is given (no username or other data)
            if len(request.data["selected_genres"]) == 2:
                recString = Recommender.recommend({}, default_list, mediaTypes, max_results, max_genres)
            # If genres only are given
            else:
                recString = Recommender.recommend({}, json.loads(request.data["selected_genres"]), mediaTypes, max_results, max_genres)
            return Response(recString)

        # If user provides a username and (optionally) some genres
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            selectedGenres = []
            if(serializer.data["selected_genres"]):
                selectedGenres = json.loads(serializer.data["selected_genres"])
            #Database.updateDB(2500)  #Adds/replaces first 2500 most popular shows on MAL.
            userList = Recommender.getList(serializer.data["userName"])
            # Below, we limit ourselves to 20 top entries, and 5 genres.
            # Selected genres is based off the client-side genre dropdown, and will replace generated genres
            recString = Recommender.recommend(userList, selectedGenres, mediaTypes, max_results, max_genres)

            return Response(recString)
