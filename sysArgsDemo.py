# search file for Keywords
import sys


json_file_name = "sample_data.json"


def read():
    file1 = open(json_file_name, 'r')
    Lines = file1.readlines()
    print(sys.argv[1:])

if __name__ == "__main__":
    read()