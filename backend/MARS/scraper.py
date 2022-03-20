import malclient
import requests
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
    return names

with open("users.txt", "w") as f:
    while True:
        names = scrapeUsers()
        print(names)
        for name in names:
            f.write(name + "\n")
            f.flush()
        time.sleep(5)