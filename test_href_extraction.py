#!/home/cyrill/anaconda3/bin/python
from bs4 import BeautifulSoup

data = '''<div class="image">
        <a href="http://www.example.com/eg1">Content1<img  
        src="http://image.example.com/img1.jpg" /></a>
        </div>
        <div class="image">
        <a href="http://www.example.com/eg2">Content2<img  
        src="http://image.example.com/img2.jpg" /> </a>
        </div>'''

soup = BeautifulSoup(data, 'html.parser')

for div in soup.findAll('div', attrs={'class':'image'}):
    print(div.find('a')['href'])
    print(div.find('a').contents[0])
