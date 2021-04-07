#!/home/cyrill/anaconda3/bin/python
#TOD: 
# for each object, download the imgage to foler. 
			# the only problem will be to accounf for irregularities, that is, dead links and things like that. 
			# but this will be quite easy.


from bs4 import BeautifulSoup

filename = '../verlauf/verlauf_trimmed.html'
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
        self.title = name
        self.url = url

        self.thumbnail = "http://img.youtube.com/vi/" + "/maxresdefault.jpg"



def extract_Names(filename):
	data = soup = BeautifulSoup(open(filename), "html.parser")
	for div in soup.findAll('div', attrs={'class':'content-cell'}):
			
			#create Entry object, and add all the objects to array.
			url = div.find('a')['href']
			content = div.find('a').contents[0]
			entr = Entry(content, url)
			my_objects.append(entr)



if __name__ == "__main__":
	getLinks(link_file)