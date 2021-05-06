import math
import json
import urllib.request
import urllib.error
import io
import array
import os

from lszz.compress import compress
from PIL import Image

twitchUrl1 = "https://static-cdn.jtvnw.net/emoticons/v1/{}/1.0"
twitchUrl2 = "https://static-cdn.jtvnw.net/emoticons/v1/{}/2.0"
twitchUrl3 = "https://static-cdn.jtvnw.net/emoticons/v1/{}/3.0"
ffzUrl = "https://cdn.frankerfacez.com/emoticon/{}/{}"
currentDir = os.path.dirname(__file__)
twitchEmotesFilePath = os.path.join(currentDir, 'emotes.json')
ffzEmotesFilePath = os.path.join(currentDir, 'ffz.json')
offlineEmotesFilePath = os.path.join(currentDir, 'offlineEmotes.json')

with open(twitchEmotesFilePath) as file:
    data = json.load(file)
codeToId = {i["code"]: i["id"] for i in data}

with open(ffzEmotesFilePath) as ffzFile:
    ffzCodeData = json.load(ffzFile)

with open(offlineEmotesFilePath) as offEmotesFile:
    offlineEmotes = json.load(offEmotesFile)

def tile(im):
    tiled = []
    tileSize = 8
    horizontalTileCount = im.size[0]/8
    verticalTileCount = im.size[0] / 8
    data = list(im.getdata())
    for i in range(math.floor(horizontalTileCount)):
        for j in range(math.floor(verticalTileCount)):
            for k in range(tileSize*tileSize):
                tiled.append(data[
                                 math.floor(i*im.size[0]*tileSize + # for each vertical tile
                                            j*tileSize + # for each horizontal tile
                                            k%tileSize + # for each horizontal pixel in each tile
                                            math.floor(k/tileSize)*im.size[0]) # for each vertical pixel in each tile
                             ])
    tiledAsBytes = []
    for i in range(0, len(tiled), 2):
        tiledAsBytes.append(tiled[i] + tiled[i + 1] * 16)

    return tiledAsBytes

def toXRGB(pal):
    ret = []
    for i in range(15):
        ret.append([pal[(3*i)+2], pal[(3*i)+1], pal[3*i]])
    return ret

def shorten(bytes):
    ret = []
    for i in range(len(bytes)):
        twoBytes = (bytes[i][0] >> 3 << 10) + (bytes[i][1] >> 3 << 5) + (bytes[i][2] >> 3)
        ret.append([twoBytes & 0xFF, twoBytes >> 8])
    return ret

def downloadTwitchEmote(emoteName):
    emoteId = codeToId[emoteName]
    try:
        return urllib.request.urlopen(twitchUrl3.format(emoteId)).read()
    except:
        print("No 4x res image for {emoteName}")
    #try 2x res
    try:
        return urllib.request.urlopen(twitchUrl2.format(emoteId)).read()
    except:
        print("No 2x res image for {emoteName}")
    #try 1x res
    try:
        return urllib.request.urlopen(twitchUrl1.format(emoteId)).read()
    except:
        print("No image for {emoteName}")
    #return None if no image found
    return None

def downloadFfzEmote(emoteName):
    emoteId = ffzCodeData[emoteName]
    try:
        return urllib.request.urlopen(ffzUrl.format(emoteId, 4)).read()
    except urllib.error.HTTPError: # some ffz emotes don't have a x4 res
        try:
            return urllib.request.urlopen(ffzUrl.format(emoteId, 2)).read()
        except urllib.error.HTTPError: # some ffz emotes don't have a x2 res
            return urllib.request.urlopen(ffzUrl.format(emoteId, 1)).read()

def getOfflineEmote(emoteName):
    eCode = emoteName[6:].lower()
    if eCode in offlineEmotes:
        return open(offlineEmotes[eCode], "rb").read()
    else:
        return None

def downloadEmote(emoteName):
    if emoteName in ffzCodeData:
        return downloadFfzEmote(emoteName)
    elif emoteName in codeToId:
        return downloadTwitchEmote(emoteName)
    else:
        return None

def getEmote(emoteName):
    rawDownload = downloadEmote(emoteName)
    if rawDownload == None:
        raise NoEmoteException()
    bytes = io.BytesIO(rawDownload)
    rawImage = Image.open(bytes).resize((64,64)).convert('RGBA')
    #mask = rawImage
    #if rawImage.mode != 'RGBA':
    #    mask = rawImage.convert('RGBA')

    # composite must have mask image of mode "1" "L" or "RGBA"
    bmpImage = Image\
        .composite(rawImage, Image.new('RGB', rawImage.size, (0,0,0)), rawImage)\
        .convert('P', palette=Image.ADAPTIVE, colors=15) # adding a black background can give images "outlines"
    #bmpImage = rawImage.convert('P', palette=Image.ADAPTIVE, colors=15) # adding a black background can give images "outlines"
    bmpImage.putpalette([255,0,0] + bmpImage.getpalette()[:-3]) # make space for the alpha color. I'm using red just for debugging visualization purposes
    bmpImage.putdata([i+1 for i in bmpImage.getdata()])

    bmpData = bmpImage.getdata()
    pngData = rawImage.getdata()

    bmpImage.putdata([0 if pngData[i][3] == 0 else bmpData[i] for i in range(len(pngData))])

    palette = bmpImage.getpalette()
    xRGB = toXRGB(palette)
    shortenedPalette = shorten(xRGB)
    flattenedPalette = [x for y in shortenedPalette for x in y]

    icon = bmpImage.copy().resize((32, 32))

    tiledBytes = tile(bmpImage)
    tileIconBytes = tile(icon)

    compressedPalette = io.BytesIO()
    compress(flattenedPalette, compressedPalette)
    compressedBytes = io.BytesIO()
    compress(tiledBytes, compressedBytes)
    iconBytes = io.BytesIO(array.array('B', tileIconBytes))

    return compressedPalette, compressedBytes, iconBytes

if __name__ == "__main__":
    getEmote("theosPaint")

class NoEmoteException(Exception):
    pass