#!/home/cyrill/anaconda3/bin/python
#TOD: 
# for each object, download the imgage to foler. 
			# the only problem will be to accounf for irregularities, that is, dead links and things like that. 
			# but this will be quite easy.
import urlparse

from bs4 import BeautifulSoup

filename = '../verlauf/verlauf_trimmed.html'

test_filename_div = '../verlauf/test.html'
link_file = 'links.txt'
my_objects = []

def extract_div(filename):
	soup = BeautifulSoup(open(filename), "html.parser")
	for link in soup.find_all('a'):
		print(link.get('href'))

def getLinks(link_file):

	file1 = open(link_file, 'r')
	Lines = file1.readlines()
	 
	count = 0
	# Strips the newline character
	for line in Lines:
		count += 1
		line = line.strip()
		if "channel/" not in line:
			#print("Line{}: {}".format(count, line.strip())) # get only the videos, not the channels
			print(line.strip())

class Entry:
	title = ""
	url = ""
	thumbnail = ""
	
	def __init__(self, title, url):
		self.title = ''.join(title).encode('utf-8').strip()
		self.url = ''.join(url).encode('utf-8').strip()
		# parse url
		url_data = urlparse.urlparse(url)
		query = urlparse.parse_qs(url_data.query)
		yt_id = query["v"][0]
		thumbnail_string = "http://img.youtube.com/vi/" + yt_id + "/maxresdefault.jpg"
		self.thumbnail = ''.join(thumbnail_string).encode('utf-8').strip()
	def __str__(self):
		return "Title: {} Url:  {}".format(self.title, self.url)
		#return "Title: {} Url:  {} thumbnail: {}".format(self.title, self.url, self.thumbnail)


def createObjects(filename):
	data = soup = BeautifulSoup(open(filename), "html.parser")
	for div in soup.findAll('div', attrs={'class':'content-cell'}):
			
			#create Entry object, and add all the objects to array.

			failed = False
			try:
				url = div.find('a')['href']
				content = div.find('a').contents[0]
			except Exception as e:
				failed = True

			if not failed:
				entr = Entry(content, url)
				my_objects.append(entr)



if __name__ == "__main__":
	createObjects(test_filename_div)
	for entry in my_objects:
		attrs = vars(entry)
		# now dump this in some way or another
		print(', '.join("%s: %s" % item for item in attrs.items()))
		print('\n')