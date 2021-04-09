#!/home/cyrill/anaconda3/envs/youtube_history_extractor/bin/python

import json
import requests
json_file_name = "sample_data.json"
file1= open(json_file_name, 'r')
Lines = file1.readlines()
jsonList = [] # Initialize emtpy list
count = -1
for line in Lines:
	count = count + 1
	#print(line)
	try:
		data = json.loads(line) # sucessfully loaded a json objet. note there is also json.load without an 's'
		jsonList.append(data)
	except Exception as e:
		print(e)
		
c = 0
for dic_t in jsonList:
	print(dic_t["thumbnail"])
	url = dic_t["thumbnail"]
	try:
		r = requests.get(url, allow_redirects=True)
		file_name_to_write = "{}{}".format("thumbnail",c)
		open(file_name_to_write, 'wb').write(r.content)
	except Exception as e:
		print("{}{}".fomat("failed, here is the iteration", c))
		raise e
	c = c+1

#idea. Json can also be avoided, and just use python dict I think.... This would simplify the code tremendously
#consider: Some objects may have not the expected values.
# Test this! If it occurs, this incidence should not confound the correct chronological order. Just jump to the next one.


