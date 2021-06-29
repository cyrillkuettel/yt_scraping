import urllib3


class Entry:  # Stores a single Video. information [title, url ,thumbnail, channelUrl] is added to attributes.
    # What I don't like is that we are using the Entry class for two use cases right now.
    # In the process we are creating a lot of redundancy
    title = ""
    url = ""
    thumbnail = ""
    channelUrl = ""

    def __str__(self):
        return "Entry Object: Title: {} Url:  {}, thumbnailUrl : {}".format(self.title, self.url, self.thumbnail)

    def extractYoutubeIdFromUrl(self):
        failed = False
        try:
            url_data = urllib3.parse_url(self.url)
        except Exception as e:
            failed = True
        try:
            query = urllib3.parse_url.parse_qs(url_data.query)
        except Exception as e:
            failed = True

        try:
            yt_id = query["v"][0]  # ?? who knows what this does, one can only guess
        except Exception as e:
            failed = True
        if not failed:
            return yt_id
        else:
            return "ID_extraction_Failed"

    def __init__(self, title, url, thumbnail):
        self.title = title
        self.url = url
        self.thumbnail = thumbnail

    # similar to Overloading a constructor, the pythonic way. this one we will use when inputting from raw html
    @classmethod
    def withChannelUrl(self, title, url, channelUrl):
        title = title.replace('\n', '')
        title = re.sub(' +', ' ', title)  # remove whitespace in the middle
        self.title = ''.join(title).encode('utf-8').strip()
        self.url = ''.join(url).encode('utf-8').strip()
        self.channelUrl = ''.join(channelUrl).encode('utf-8').strip()

        yt_id = self.extractYoutubeIdFromUrl()

        if not yt_id == "ID_extraction_Failed":  # 99% of the time it's possible to craft the link for thumbnail.
            thumbnail_string = "http://img.youtube.com/vi/" + yt_id + "/0.jpg"
            self.thumbnail = ''.join(thumbnail_string).encode('utf-8').strip()
        else:
            self.thumbnail = yt_id