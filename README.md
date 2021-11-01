# Scrape your Youtube Profile
**WARNING! This is still in development.**



It's a youtube history viewer, with some pretty diagramms basically. 
I'm writing this application to be able to instantly search my youtube history. 
This is all possible thanks to [Google Takeout](https://takeout.google.com/settings/takeout), which enables users to export data from their google accounts. 

# How to run
1. Install conda and clone the environment 
```
conda env create --file environment.yml
conda env activate <name-of-environent>

```
2. Run extracting_data.py using python3.5
```
python3.5 extracting_data.py
```


yt_scraping is planned to include the features
- [x] search instantly
- [x] generate pretty Wordclouds
- [x] automatically and concurrently download the thumbnails
- [ ] advanced text search 
- [ ] approximate string matching [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance)
- [ ] full text search (based on the subtitles)
- [ ] read the 10mb html hitory file with a little bit of parallelism/multiprocessing




(these are not the selling points, but rather milestones of the development)


![screnshot](img/screenshot.png)



