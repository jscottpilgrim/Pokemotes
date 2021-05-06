import json
import glob

filelist = glob.glob('./emotes*.json')

def combine():
    result = []

    for file in filelist:
        with open(file) as f:
            data = json.load(f)
        result = result + data

    with open('combined.json', 'w') as outfile:
            json.dump(result, outfile)

if __name__ == "__main__":
    combine()