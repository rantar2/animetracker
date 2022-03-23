from urllib import request, response
from .models import AnimeEntry,Genre
from .MARSdb import Database
import secrets
import requests


clientID = "54082defd56574106879639dd3f91e47"
clientSecret = "ab20781868791a1ab2999c963953048d20cfd353d9d3ba98a9b06717caa73657"


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

    def recommend(userList, reclimit, genrelimit):
        Database.updateDB(1000)  #Adds/replaces first 1000 most popular shows on MAL.

        genreDict = {}
        titleList = []
        recDict = {}
        for i in userList["data"]:
            titleList.append(i["node"]["title"])
            # Genre list influenced by user score
            for genre in i["node"]["genres"]:
                gname = genre["name"]
                # Create or update the running raw score of a certain genre.
                if not gname in genreDict:
                    genreDict[gname] = i["list_status"]["score"]
                else:
                    genreDict[gname] += i["list_status"]["score"]
        topGenres = sorted(genreDict, key=genreDict.get, reverse=True)[:genrelimit]
        recString = "Recommended Shows: \n"
        for genre in topGenres:
            # Basic query, filter, exclude watched shows, add to recommendations.
            # Matches based on user's top genres. Definitely could be refined.
            for i in AnimeEntry.objects.filter(genres__genre_name=genre):
                if i.name not in titleList:
                    # MAL user score defines how highly a recommendation should be considered in our algorithm.
                    # Currently is pretty basic, but reasonably effective in our limited testing
                    score = 1 / (topGenres.index(genre) + 1)
                    if i.name not in recDict:
                        recDict[i.name] = score
                    else:
                        recDict[i.name] += score

        recDict = sorted(recDict, key=recDict.get, reverse=True)[:reclimit]
        for title in recDict:
            recString += title + "\n"

        return recString
