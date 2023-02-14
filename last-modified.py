import requests
import sys
import json
from time import gmtime, strftime
from urllib.parse import urlparse
from datetime import datetime

def get_date(): return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

#This will return last modified time of given web page url
def get_last_modified(url):
    #page = {'url': "", 'date': "", 'last_modified': ""}
    result = urlparse(url)
    if True if [result.scheme, result.netloc, result.path] else False:
        header = requests.head(url).headers
        if 'Last-Modified' in header:
            return header['Last-Modified']
        print("Data is not available")
        return -1
    else:
        return -1
#Demonstration of function call
if __name__ == '__main__':
#    try:
        url = sys.argv[1]
        print(get_date())
        print(get_last_modified(url))
#    except Exception as e:
        print("Please provide proper url as a first argument.")
