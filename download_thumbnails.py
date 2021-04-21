import json
import requests
import pathlib
import sys
import ctypes

json_file_name = "15k.json"  # in the future, this will be a command line argument args[]
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
            print("{}{}".format("requests failed for thumbail. Iteration =", c))
            raise e
        c = c + 1


def getID(videoUrl):
    trimBefore = videoUrl[0:32]  # Is equal to "https://www.youtube.com/watch?v="
    s = videoUrl.replace(trimBefore, "")
    return s


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


def wordCounter(jsonList):
    searchString = ' '.join(sys.argv[1:])
    inputArgs = sys.argv
    results = []
    for i in inputArgs[1:]:  # Loop Through input args
        results.append(ForEachTitleDoesContainWord(jsonList, i))
    print(results)  # Prints how many time each word occurred


# @returns prevalence of searchString
def ForEachTitleDoesContainWord(jsonList, searchString):
    count = 0
    for dic_t in jsonList:
        title = getID(dic_t["title"])
        if searchString in title:
            count += 1
    return count


if __name__ == "__main__":
    jsonList = loadEachVideoAsJsonIntoArray(Lines)
    wordCounter(jsonList)
# downloadThumbnails(jsonList)


# idea. Json is not really necessary , and just use python dict I think.... This would simplify the code tremendously
# consider: Some objects may have not the expected values. Test this! If it occurs, this incidence should not
# confound the correct chronological order. Just jump to the next one.

#  TODO: 
# Make Case-Insensitive