#!/usr/bin/env python

import sys
import os
from time import gmtime, strftime
from urllib.parse import urlparse
from datetime import datetime
import requests
import mysql.connector

def convert_str2date(strdate):
    return datetime.strptime(strdate.replace(' GMT', ''),
                             "%a, %d %b %Y %H:%M:%S").date()


def get_date(): return strftime("%Y-%m-%d", gmtime())


def check_http(url):
    if not 'http:' in url:
        url = 'http://' + url

    return url
    

def get_last_modified(url):
    page = {}
    try:
        url = check_http(url)
        check_response = requests.get(url, allow_redirects=True, timeout=10)
        result = urlparse(check_response.url)
        if [result.scheme, result.netloc, result.path]:
            header = requests.head(url, allow_redirects=True, timeout=10).headers
            if 'Last-Modified' in header:
                page["url"] = url
                page["date"] = get_date()
                page["last_modified"] = convert_str2date(header['Last-Modified'])
                page["error"] = 0
            else:
                page["url"] = url
                page["date"] = get_date()
                page["error"] = 1
    except Exception:
        page["url"] = url
        page["date"] = get_date()
        page["error"] = 1
    return page


if __name__ == '__main__':
    try:
        pages_path = sys.argv[1]
        if not os.path.exists(pages_path):
            print(f'O arquivo {pages_path} nao foi encontrado.')
            sys.exit(1)

        urls = None
        page = None
        with open(pages_path, 'r', encoding='utf-8') as pages_file:
            urls = pages_file.readlines()


        cnx = mysql.connector.connect(user='ticweb',
                                      database='ticweb_a11y',
                                      port='6033',
                                      password='K4RN4Vu')
        cursor = cnx.cursor()

        for url in urls:
            page = get_last_modified(url.rstrip())

            columns = ', '.join("`" + str(x) + "`" for x in page.keys())
            values = ', '.join("'" + str(x) + "'" for x in page.values())

            add_page = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('pages', columns, values)
            #print(add_page)

            cursor.execute(add_page, page.values())
            cnx.commit()

        cursor.close()
        cnx.close()

    except IndexError:
        print("Please provide proper url as a first argument.")
    except ValueError:
        print("Get url last modified info error.")
