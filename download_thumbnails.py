import json
import requests
import pathlib

json_file_name = "sample_data.json"  # in the future, this will be a command line argument args[]
file1 = open(json_file_name, 'r')
Lines = file1.readlines()


def loadEachVideoAsJsonIntoArray(Lines):
    jsonList = []
    for line in Lines:
        print(line)
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
    for dic_t in jsonList:  # each object in array jsonList is basically a python dicitonary
        videoId = getID(dic_t["url"])
        completePath = folderName + "_" + videoId  # just use os.path for this.
        url = dic_t["thumbnail"]
        try:
            r = requests.get(url, allow_redirects=True)  # instead of c, use the id of this particular video
            open(completePath, 'wb').write(r.content)
        except Exception as e:
            print("{}{}".format("requests failed for thumbail. Iteration =", c))
            raise e
        c = c + 1


def getID(videoUrl):
    trimBefore = videoUrl[0:32]  # Is equal to "https://www.youtube.com/watch?v="
    s = videoUrl.replace(trimBefore, "")
    return s


if __name__ == "__main__":
    jsonList = loadEachVideoAsJsonIntoArray(Lines)
    downloadThumbnails(jsonList)

# TODO:
# it does not save thumbnails in the specified folder

# idea. Json is not really necessary , and just use python dict I think.... This would simplify the code tremendously
# consider: Some objects may have not the expected values.
# Test this! If it occurs, this incidence should not confound the correct chronological order. Just jump to the next one.
