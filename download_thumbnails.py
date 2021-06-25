import json
import requests
import pathlib
import sys

json_file_name = "15k.json"  # in the future, this will be a command line argument args[]
# I think his class is essentially only used in the initial phase, when the history file is first opened.
file1 = open(json_file_name, 'r')
Lines = file1.readlines()


def loadEachVideoAsJsonIntoArray(Lines):
    jsonList = []
    for line in Lines:
        # print(line)
        try:
            data = json.loads(line)  # successfully loaded a json objet. note there is also json.load without an 's'
            jsonList.append(data)
        except Exception as e:
            print("{} {}".format("could not load json for this video. Probably url not valid. ", e))
    return jsonList


def downloadThumbnails(jsonList):
    folderName = "thumbnails"
    pathlib.Path(folderName).mkdir(parents=True, exist_ok=True)  # create the folder
    c = 0
    for dic_t in jsonList:  # each object in array jsonList is basically a python dictionary
        videoId = getID(dic_t["url"])
        completePath = folderName + '/' + folderName + "_" + videoId  # just use os.path for this.
        thumbnailUrl = dic_t["thumbnail"]
        try:
            r = requests.get(thumbnailUrl, allow_redirects=True)
            open(completePath, 'wb').write(r.content)
        except Exception as e:
            print("{}{}".format("requests failed for thumbnail. Iteration =", c))
            raise e
        c = c + 1


def getID(videoUrl):
    trimBefore = videoUrl[0:32]  # Is equal to "https://www.youtube.com/watch?v="
    s = videoUrl.replace(trimBefore, "")
    return s


# TODO:
#  Make Case-Insensitive
def searchKeyword(jsonList):
    searchString = ' '.join(sys.argv[1:])
    print(searchString)
    count = 0
    for dic_t in jsonList:
        title = getID(dic_t["title"])
        if searchString in title:
            count += 1
            print(dic_t)
    print("found = {} occurrences".format(count))


# Prints how many time each word occurred
def wordCounter(jsonList):
    results = []
    for i in sys.argv[1:]:  # Loop Through input args
        results.append(ForEachTitleDoesContainWord(jsonList, i))
    print(results)


# @returns prevalence of searchString
def ForEachTitleDoesContainWord(jsonList, searchString):
    count = 0
    for dic_t in jsonList:
        title = getID(dic_t["title"]) # ???? why did I write getID here. This returns the ID of the title?
        if searchString in title:
            count += 1
    return count


if __name__ == "__main__":
    jsonList = loadEachVideoAsJsonIntoArray(Lines)

# idea. Json is not really necessary , and just use python dict I think.... This would simplify the code tremendously
# consider: Some objects may have not the expected values. Test this! If it occurs, this incidence should not
# confound the correct chronological order. Just jump to the next one.
#

# Initially: Load the html raw data. Then feed that into python dict. And maybe, parallel, thumbnails download
