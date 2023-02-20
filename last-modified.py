import requests
import sys
import json
from time import gmtime, strftime
from urllib.parse import urlparse
from datetime import datetime
import mysql.connector

def convert_str2date(strdate):
    return datetime.strptime(strdate.replace(' GMT', ''), "%a, %d %b %Y %H:%M:%S").date()

def get_date(): return strftime("%Y-%m-%d", gmtime())

def get_last_modified(url):
    page = {}
    try: 
        result = urlparse(url)
        if [result.scheme, result.netloc, result.path]:
            header = requests.head(url).headers
            if 'Last-Modified' in header:
                page["url"] = url
                page["date"] = get_date()
                page["last_modified"] = convert_str2date(header['Last-Modified'])
                page["error"] = 0
    except Exception:
        page["url"] = url
        page["date"] = get_date()
        page["error"] = 1
    
    return page
if __name__ == '__main__':
    try:
        url = sys.argv[1]
        print(get_last_modified(url))
        cnx = mysql.connector.connect(user='ticweb', database='ticweb_a11y', port='6033', password='K4RN4Vu')
        cursor = cnx.cursor()

        page = get_last_modified(url)

        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in page.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in page.values())

        add_page = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('pages', columns, values)
        print(add_page)

        cursor.execute(add_page, page.values())

        cnx.commit()
        cursor.close()
        cnx.close()

    except IndexError: 
        print("Please provide proper url as a first argument.")
    except ValueError:
        print("Get url last modified info error.")
