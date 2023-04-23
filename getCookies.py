import requests
import sqlite3
import json
import sys

def CreateCookiesForSession(cursor:sqlite3.Cursor, host_key:str) -> "list[dict]":
    """
    returns a list of all cookies for a certain host key.
    cursor is an sqlite3 cursor.
    host_key is the host_key for the website we are trying to parse.
    """
    cursor.execute('SELECT name, value FROM cookies WHERE host_key LIKE ? || "%%"', ('%' + host_key + '%',))

    cookieList:"list[dict]" = []
    for name, value in cursor.fetchall():
        cookie:dict[str, str] = {
            'name':name,
            'value':value,
        }
        cookieList.append(cookie)
    return cookieList

def ConvertCookiesToString(cookies:"list[dict]") -> "str":
    cookieList = []
    for cookie in cookies:
        cookieStr = ""
        cookieStr += cookie['name']
        cookieStr += "="
        cookieStr += cookie['value']
        cookieList.append(cookieStr)
    return json.dumps(cookieList)

def GetCookies(domain:str) -> str:
    # Connect to the Database
    conn = sqlite3.connect('./Cookies')
    cursor = conn.cursor()

    cookies = CreateCookiesForSession(cursor, domain)
    cookieList = ConvertCookiesToString(cookies)
    return cookieList

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("PLEASE PROVIDE A LIST OF DOMAINS TO GET COOKIES FOR")
    else:
        print('*'*120)
        for domain in sys.argv[1:]:
            cookie = GetCookies(domain)
            print('DOMAIN: ' + domain)
            print(cookie)
            print('*'*120)
