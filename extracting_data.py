#!/home/cyrill/anaconda3/envs/youtube_history_extractor/bin/python

import urllib3
import json
import re

from bs4 import BeautifulSoup

verlauf_trimmed = '../verlauf/verlauf_trimmed.html'

test_filename_div = '../verlauf/test_filename_div.html'
link_file = 'link_file.txt'
my_objects = []



class Entry: # Stores a single Video. information [title, url thumbnail] is added to attributes.
	title = ""
	url = ""
	thumbnail = ""

	def extractYoutubeIdFromUrl(self):
		failed = False
		try:
			url_data = urlparse.urlparse(self.url)
		except Exception as e:
			failed = True
	
		try:
			query = urlparse.parse_qs(url_data.query)
		except Exception as e:
			failed = True
		
		try:
			yt_id = query["v"][0]
		except Exception as e:
			failed = True
		if not failed:
			return yt_id
		else:
			return "ID_extraction_Failed"

	def __init__(self, title, url):

		title = title.replace('\n','')
		title =  re.sub(' +', ' ', title) # remove whitspace in the middle
		self.title = ''.join(title).encode('utf-8').strip()
		self.url = ''.join(url).encode('utf-8').strip()
		
		yt_id = self.extractYoutubeIdFromUrl()

		if yt_id == "ID_extraction_Failed":
			self.thumbnail = "ID_extraction_Failed"
		else:
			thumbnail_string = "http://img.youtube.com/vi/" + yt_id + "/maxresdefault.jpg"
			self.thumbnail = ''.join(thumbnail_string).encode('utf-8').strip()



#create Entry object, and add all the objects to array my_objects.
def createObjects(filename): # create the array Of "json objects"
	data = soup = BeautifulSoup(open(filename), "html.parser")
	print("{")
	for div in soup.findAll('div', attrs={'class':'content-cell'}):#selects the div which is imporant
			failed = False
			try:
				url = div.find('a')['href']
				title = div.find('a').contents[0]
				if "https://www.youtube.com" in title: # avoid delete Videos
					failed = True
			except Exception as e:
				failed = True

			if not failed:
				entry = Entry(title, url)
				#my_objects.append(entr)
				print(json.dumps(vars(entry)))
	print("}") #close the json object


#Various methods, not currently in use
def extract_div(filename):
	soup = BeautifulSoup(open(filename), "html.parser")
	for link in soup.find_all('a'):
		print(link.get('href'))

def getOnlyVideoLinks_notChannel(link_file):

	file1 = open(link_file, 'r')
	Lines = file1.readlines()
	 
	count = 0
	# Strips the newline character
	for line in Lines:
		count += 1
		line = line.strip()
		if "channel/" not in line: # 
			#print("Line{}: {}".format(count, line.strip())) # Interesting .format() idea which might be useful later. 
			print(line.strip())


if __name__ == "__main__":
	createObjects(test_filename_div)
