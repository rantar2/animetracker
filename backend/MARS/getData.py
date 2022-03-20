from urllib import request, response
from .models import AnimeEntry
import malclient
import secrets
import requests
import base64
import json
import time

def scrapeUsers():
    url = "https://myanimelist.net/users.php"
    names = []
    response = requests.get(url)
    startIndex = 0
    for j in range(0, 20):
        k = response.text.find("<div class=\"picSurround\"><a href=\"/profile/", startIndex)
        if(k != -1):
            curName = ""
            k += 43
            while(response.text[k] != "\""):
                curName += response.text[k]
                k += 1
            names.append(curName)
            startIndex = k
        else:
            break
    print(names)
    return names