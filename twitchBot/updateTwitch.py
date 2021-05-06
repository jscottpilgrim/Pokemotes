import urllib.request
import json
import os
import time

url = "https://api.twitchemotes.com/api/v4/emotes?id="

def getAllEmotes():

    # as of 2021/03/24 it looks like all emotes are in two batches of id numbers:
    # 1000000 - 3000000
    # 300000000 - 310000000
    current = 0
    end = 400000000
    emotesList = []
    consecutiveBlankCount = 0
    consecutiveFailCount = 0

    while current < end: #True:
        print(current)
        url = "https://api.twitchemotes.com/api/v4/emotes?id=" + str(current)
        for i in range(current+1, current+100):
            url += "," + str(i)
        try:
            result = json.loads(urllib.request.urlopen(url).read())
        except:
            print(f"API request failed at id {current}")
            consecutiveFailCount += 1
            time.sleep(2)
            if consecutiveFailCount >= 20:
                print(f"20 consecutive failures at id {current}")
                inp = input("Retry? (y/n): ")
                if inp.lower() == "y":
                    continue
                else:
                    end = current
                    break
            continue
        if len(result) == 0:
            consecutiveBlankCount += 1
            if consecutiveBlankCount >= 10000000:
                end = current
                break
        else:
            emotesList = emotesList + result
            consecutiveBlankCount = 0
        current += 100
        consecutiveFailCount = 0

        #save 1mil per file
        if current % 1000000 == 0:
            print(f"writing to file at id {current}")
            with open(f"emotes{current}.json", 'w') as outfile:
                json.dump(emotesList, outfile)
            emotesList = []

    print(f"Ended at id {end}")

if __name__ == "__main__":
    getAllEmotes()