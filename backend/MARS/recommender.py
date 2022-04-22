from urllib import request, response
from .models import AnimeEntry,Genre
from .MARSdb import Database
from .serializers import *
from rest_framework.renderers import JSONRenderer
import secrets
import requests


clientID = "54082defd56574106879639dd3f91e47"
clientSecret = "ab20781868791a1ab2999c963953048d20cfd353d9d3ba98a9b06717caa73657"

# Recommender responsibilities: return a user's list from MAL (getList), and make recommmendations for the user (recommend)
class Recommender:
    def getList(username):
        """
        Gets a public MAL user's list.
        Anime entries returned are formatted as follows:
        "data":{
            "node":{
                "id":420,
                "title":"watashi no anime",
                "main_picture":{"medium":"https://...","large":"https://..."},
                "genres":[{"id":69, "name":"slice of life"},...]
                "list_status":{"status":"completed","score":10...}
                }
            }

        """
        # Retrives the above data from up to 1000 of the user's completed shows.
        url = f"https://api.myanimelist.net/v2/users/{username}/animelist?fields=list_status,genres&sort=list_score&limit=1000&status=completed"
        response = requests.get(url, headers= {
            "X-MAL-CLIENT-ID": clientID
        })
        response.raise_for_status()
        userList = response.json()
        response.close()

        return userList

    def recommend(userList, selectedGenres, mediaTypes, recLimit, genreLimit):
        # First creates a top genres list
        genreDict = {}
        titleList = []
        recDict = {}
        recScores = {}
        topGenres = selectedGenres

        # Create a top genres list containing either the user selected genres or the algorithmically decided best genres
        if len(userList.items()) != 0:
            for i in userList["data"]:
                titleList.append(i["node"]["title"])
                # Genre list influenced by user score
                for genre in i["node"]["genres"]:
                    gname = genre["name"]
                    # Create or update the running raw score of a certain genre.
                    score = i["list_status"]["score"] * i["list_status"]["score"]
                    # Weigh a genre lower if it's a very broad category
                    if(gname == "Fantasy" or gname == "Action" or gname == "Comedy"):
                        score *= 0.85
                    if not gname in genreDict:
                        genreDict[gname] = score
                    else:
                        genreDict[gname] += score
        autoGenres = {k: v for k, v in sorted(genreDict.items(), key=lambda item:item[1], reverse=True)}
        # Add auto generated genre items if the user provides less than the limit of genres.
        # The user can add as many as they want, but if the limit is surpassed,
        # auto genres are ignored.
        for item in autoGenres:
            if len(topGenres) >= genreLimit:
                break
            if item not in topGenres:
                topGenres.append(item)
        # Initialize the recommendations string (a JSON list of objects) and score shows based on how well they match the user criteria
        recString = "{\"anime\":["
        for genre in topGenres:
            # Basic query, filter, exclude watched shows, add to recommendations.
            # Matches solely based on user's top genres. Definitely could be refined.
            for i in AnimeEntry.objects.filter(genres__genre_name=genre):
                skip = (i.media_type == "tv" and mediaTypes[0] == False or
                        i.media_type == "movie" and mediaTypes[1] == False or
                        i.media_type == "special" and mediaTypes[2] == False or
                        i.media_type == "ova" and mediaTypes[3] == False or
                        i.media_type == "ona" and mediaTypes[4] == False or
                        i.media_type == "music" or
                        i.media_type == "unknown")

                if i.name not in titleList and not skip:
                    # MAL user score defines how highly a recommendation should be considered in our algorithm.
                    # Currently is pretty basic, but reasonably effective in our limited testing
                    score = 1 / (topGenres.index(genre) + 1) * 1.5
                    # Lower inital scores for genres people most likely won't be interested in
                    if(genre != "Kids" and i.genres.filter(genre_name="Kids").exists()):
                        score /= 2

                    if i.name not in recDict:
                        recDict[i.name] = score
                        recScores[i.name] = i.score
                    else:
                        recDict[i.name] += score
                        recScores[i.name] = i.score

        # Go through recDict, this time increasing the score based on how highly rated the show is
        for show in recDict:
            # Add to this score based on how highly rated the show is
            # Formula (s = average user score): |(s-7)|/(s-7) * (s-7)^2 / 9
            # First section gets the sign of s-7, the second segment biases towards higher rated shows
            s = recScores[show]
            if(s != 7):
                recDict[show] += ((abs(s - 7)/(s - 7)) * (s - 7) * (s - 7)) / 4

        # Sort the shows by their score and finialize the recommendations string to send to client
        print(topGenres)
        recDict = sorted(recDict, key=recDict.get, reverse=True)[:recLimit]
        for title in recDict:
            anime = AnimeEntry.objects.get(name=title)
            serializer = AnimeSerializer(anime)
            #print(serializer.data)
            content = JSONRenderer().render(serializer.data).decode("utf-8")
            recString += content + ","
        recString = recString[:-1]
        recString += "]}"
        return recString
