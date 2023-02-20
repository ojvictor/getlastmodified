import requests
import sys
import json
from time import gmtime, strftime
from urllib.parse import urlparse
from datetime import datetime

def get_date(): return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

def get_last_modified(url):
    page = {'url': "", 'date': "", 'last_modified': "", 'error': False}
    try: 
        result = urlparse(url)
        if [result.scheme, result.netloc, result.path]:
            header = requests.head(url).headers
            if 'Last-Modified' in header:
                page["url"] = url
                page["date"] = get_date()
                page["last_modified"] = header['Last-Modified']
                page["error"] = False
    except Exception:
        page["url"] = url
        page["date"] = get_date()
        page["last_modified"] = None
        page["error"] = True
        
    return json.dumps(page, indent = 2)
if __name__ == '__main__':
    try:
        url = sys.argv[1]
        print(get_last_modified(url))
    except IndexError: 
        print("Please provide proper url as a first argument.")
    except ValueError:
        print("Get url last modified info error.")
