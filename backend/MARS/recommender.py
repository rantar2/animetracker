from urllib import request, response
from .models import AnimeEntry,Genre
from .getData import scrapeUsers
import malclient
import secrets
import requests

# Notice: This should all be refactored into classes later

# dictionary of all shows, contains key value pair of show and how high its scored

clientID = "54082defd56574106879639dd3f91e47"
clientSecret = "ab20781868791a1ab2999c963953048d20cfd353d9d3ba98a9b06717caa73657"

def getList(username):
    # We can add whatever fields we need to the url later
    url = f"https://api.myanimelist.net/v2/users/{username}/animelist?fields=genres&sort=list_score&limit=1000"
    response = requests.get(url, headers= {
        "X-MAL-CLIENT-ID": clientID
    })
    response.raise_for_status()
    userList = response.json()
    """
    # Anime entries are formatted like a dictionary as follows:
    "data":{
        "node":{
            "id":420,
            "title":"watashi no anime",
            "main_picture":{"medium":"https://...","large":"https://..."},
            "genres":[{"id":69, "name":"slice of life"},...]
            }
        }

    """
    response.close()

    return userList

def updateDB(n):
    """
    Retrives n number of anime by ranking, then updates internal database. This
    should run regularly, but not too frequently as to avoid hitting MAL's limit
    (error handling to come later).
    """
    j = n//500  # Number of iterations
    if n%500 != 0 and j > 0:
        print(f"n should be a multiple of 500. Rounding to {j*500} entries.")
    elif j==0:
        print(f"n should be a multiple of 500. Rounding to 500 entries.")
        j=1

    """
    Anime entries returned below are as follows:
    "data":{
        "node":{
            "id":747,
            "title":"boku no anime",
            "main_picture":{"medium":"https://...","large":"https://..."},
            "genres":[{"id":69, "name":"slice of life"},...],
            }
        "ranking":{
            "rank":666
            }
        }
    This Django DB toutorial may be helpful:
    https://riptutorial.com/django/example/4015/basic-django-db-queries
    """
    for i in range(j):
        # We can specify which types of anime to index by changing the url below.
        # Currently, it retrives anime by popularity, but we can specify movies, TV series, etc
        # We can also change the "fields" to include other data.
        url = f"https://api.myanimelist.net/v2/anime/ranking?ranking_type=bypopularity&fields=genres&limit=500&offset={i*500}"
        response = requests.get(url, headers= {
            "X-MAL-CLIENT-ID": clientID
        })
        response.raise_for_status()
        animeList = response.json()
        response.close()
        for anime in animeList["data"]:
            newEntry = AnimeEntry(
                name=anime["node"]["title"],
                rank=anime["ranking"]["rank"],
                animeID=anime["node"]["id"]
            )
            newEntry.save()
            # Iterate through a show's genres, adding genres to the Genre DB
            # Also assigns genres to shows. This functionality is highly expensive.
            for g in anime["node"]["genres"]:
                gen = Genre.objects.get_or_create(genre_name=g["name"], genre_id=g["id"])
                newEntry.genres.add(gen[0])

def recommend(userList):
    scrapeUsers()
    AnimeEntry.objects.all().delete()  # Overwrite old entries. Maybe not the most efficient...
    #Genre.objects.all().delete()  # Don't need to run this, unless MAL changes lookup ids.
    updateDB(1000)  #Adds/replaces first 1000 most popular shows on MAL.

    genreDict = {}
    titleList = []
    for i in userList["data"]:
        titleList.append(i["node"]["title"])
        for genre in i["node"]["genres"]:
            gname = genre["name"]
            if not gname in genreDict:
                genreDict[gname] = 1
            else:
                genreDict[gname] += 1
    topGenres = sorted(genreDict, key=genreDict.get, reverse=True)[:6]
    statString = "Most Watched Genres: \n"
    recString = "Recommended Shows: \n"
    for genre in topGenres:
        # Basuc query, filter, exclude watched shows, add to recommendations.
        # Blindly matches based on user's top genres. Definitely could be refined.
        for i in AnimeEntry.objects.filter(genres__genre_name=genre):
            if i.name not in titleList:
                recString += i.name + "\n"
        statString += genre + "\n"
    statString += "\nTop Shows: \n"
    for i in range(0, 10):
        statString += titleList[i] + "\n"

    #print(statString)
    #print(recString)
    return recString
