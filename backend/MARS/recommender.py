from urllib import request
import malclient
import secrets
import requests

clientID = "54082defd56574106879639dd3f91e47"
clientSecret = "ab20781868791a1ab2999c963953048d20cfd353d9d3ba98a9b06717caa73657"

def getList(username):
    # We can add whatever fields we need to the url later
    url = f"https://api.myanimelist.net/v2/users/{username}/animelist?fields=genres&sort=list_score&limit=50"
    response = requests.get(url, headers= {
        "X-MAL-CLIENT-ID": clientID
    })
    response.raise_for_status()
    userList = response.json()
    response.close()

    return userList

def recommend(userList):
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
    recString = "Most Watched Genres: \n"
    for genre in topGenres:
        recString += genre + "\n"
    recString += "\nTop Shows: \n"
    for i in range(0, 10):
        recString += titleList[i] + "\n"
    

    print(recString)
    return recString