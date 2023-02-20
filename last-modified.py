import requests
import sys
import json
from time import gmtime, strftime
from urllib.parse import urlparse
from datetime import datetime

def convert_str2date(strdate):
    return datetime.strptime(strdate.replace(' GMT', ''), "%a, %d %b %Y %H:%M:%S").date()

def get_date(): return strftime("%Y-%m-%d", gmtime())

def get_last_modified(url):
    page = {'url': "", 'date': "", 'last_modified': "", 'error': False}
    try: 
        result = urlparse(url)
        if [result.scheme, result.netloc, result.path]:
            header = requests.head(url).headers
            if 'Last-Modified' in header:
                page["url"] = url
                page["date"] = get_date()
                page["last_modified"] = convert_str2date(header['Last-Modified'])
                page["error"] = False
    except Exception:
        page["url"] = url
        page["date"] = get_date()
        page["last_modified"] = None
        page["error"] = True
        
    return json.dumps(page, indent = 2, default = str)
if __name__ == '__main__':
    try:
        url = sys.argv[1]
        print(get_last_modified(url))
    except IndexError: 
        print("Please provide proper url as a first argument.")
    except ValueError:
        print("Get url last modified info error.")
