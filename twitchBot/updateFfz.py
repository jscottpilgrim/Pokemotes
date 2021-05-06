import urllib.request
import json
import os
import time

def url(page):
    return "http://api.frankerfacez.com/v1/emoticons?per_page=200&private=on&page=" + str(page)

def getAllFfz():
    try:
        os.remove('ffz.json')
    except:
        pass
    data = {}
    result = json.loads(urllib.request.urlopen(url(1)).read())
    extractData(data, result)
    pages = int(result["_pages"])
    for i in range(2, pages+1):
        tries = 0
        maxTries = 20
        while True:
            try:
                result = json.loads(urllib.request.urlopen(url(i)).read())
                break
            except:
                tries += 1
                if tries >= maxTries:
                    inp = input("Failed 20 times to get web results for page {i}. Try again? (y/n): ")
                    if inp != "y" and inp != "Y":
                        raise Exception("failed to get web results for page {i}")
                else:
                    time.sleep(60)
        extractData(data, result)
        print(str(i) + " of " + str(pages))
    with open('ffz.json', 'w') as outfile:
        json.dump(data, outfile)


def extractData(data, result):
    emotes = result['emoticons']
    for i in range(len(emotes)):
        data[emotes[i]['name']] = emotes[i]['id']

if __name__ == "__main__":
    getAllFfz()