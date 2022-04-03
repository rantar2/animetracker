from urllib import request, response
from .models import AnimeEntry,Genre
import secrets
import requests
clientID = "54082defd56574106879639dd3f91e47"


class Database:
    def updateDB(n):
        """
        Retrives n number of anime by ranking, then updates internal database. This
        should run regularly, but not too frequently as to avoid hitting MAL's limit
        (error handling to come later).

        Anime entries returned are formatted as follows:
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
        """
        print("Updating db...");
        AnimeEntry.objects.all().delete()  # Remove old entries. Maybe not the most efficient...
        Genre.objects.all().delete()  # Don't need to run this, unless MAL changes lookup ids.
        n = n//1  # Number of iterations. Floor divide to eliminate float values.
        if n<=0:
            print(f"Defaulting to 500 entries.")
            n=500

        entriesRetrived = 0
        while entriesRetrived < n:
            # We can specify which types of anime to index by changing the url below.
            # Currently, it retrives anime by popularity, but we can specify movies, TV series, etc
            # We can also change the "fields" to include other data.

            entriesToRetrive = min(500,n-entriesRetrived)
            url = f"https://api.myanimelist.net/v2/anime/ranking?ranking_type=bypopularity&fields=genres,main_picture,synopsis&limit={entriesToRetrive}&offset={entriesRetrived}"
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
                    MAL_ID=anime["node"]["id"],
                    main_picture=anime["node"]["main_picture"]["medium"],
                    synopsis=anime["node"]["synopsis"]
                )
                newEntry.save()
                # Iterate through a show's genres, adding genres to the Genre DB
                # Also assigns genres to shows. This functionality is highly expensive.
                for g in anime["node"]["genres"]:
                    gen = Genre.objects.get_or_create(genre_name=g["name"], genre_id=g["id"])
                    newEntry.genres.add(gen[0])
            entriesRetrived += entriesToRetrive
        print(f"Finished updating db. Currently contains {AnimeEntry.objects.count()} entries from {Genre.objects.count()} genres.");
