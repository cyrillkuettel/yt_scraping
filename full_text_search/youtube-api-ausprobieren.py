import sys
import requests
print("starting search . . . ")

if len(sys.argv) > 1:
    print("searching for " + sys.argv[1])
else:
    print("please supply arguments keywords!")
    exit()

Youtube_Video_ID = "tTBWfkE7BXU"

"https://video.google.com/timedtext?lang=en&v=tTBWfkE7BXU"
Video_URL = "https://video.google.com/timedtext?lang=en&v=" + Youtube_Video_ID

r = requests.get(Video_URL)
print(r.status_code)

print(r.text)
print("\n==============================================================================")
print("\nContent of the said url:")
print(r.content)
