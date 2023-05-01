from io import StringIO
import subprocess
import sys
import os
import time
import threading
from selenium import webdriver  # pip install Selenium
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import getCookies

import validators

# returns True the title changed after injection
def InjectCookiesToDomain(domain:str, automatic:bool=False, vulnList:'list[str]' = []):
    # URL to open in new window, assume https and .com
    cookies = getCookies.GetCookies(domain)

    vulnReason = ""

    if len(cookies) == 0:
        print(f"No Cookies for: {domain}")
        return

    if domain[0] != ".":
        domain = "." + domain

    url = f"https://www{domain}"
    validUrl = validators.url(url)
    if validUrl == False:
        print(f"Invalid URL: {url}")
        return

    print(f"Testing URL: {url}")
    javascriptCode = \
    f"""
    cookieStr = '{cookies}';
    cookieArr = JSON.parse(cookieStr);
    cookieArr.forEach((item) => {{
        document.cookie = item;
    }})
    """
    if automatic == False:
        print("JS code that will be injected: ")
        print(javascriptCode)
        print("*"*64)

    chromeOptions = Options()
    if automatic:
        chromeOptions.add_argument("--headless")

    chromeOptions.add_argument('--log-level=3')
    # open chrome
    driver = webdriver.Chrome(options=chromeOptions)
    driver.set_window_position(100,-1000)
    driver.implicitly_wait(1)

    # go to url
    try:
        driver.get(url)
    except WebDriverException:
        print("Failed to connect on URL: " + url)
        driver.close()
        driver.quit()
        return

    titleBeforeInjection = driver.title

    pageHtml = str(driver.page_source)
    pageHtml = pageHtml.lower()

    if (automatic == False):
        #wait for input to inject cookies
        input("Press enter to inject cookies\n")

    try:
        driver.execute_script(javascriptCode)
        driver.refresh()
    except WebDriverException:
        print("Exception when executing script: " + url)
        print(f"Script: \n{javascriptCode}")
        driver.close()
        driver.quit()
        return



    # if there was an option to login and now there isn't, assume we logged in
    newPageHtml = str(driver.page_source)
    newPageHtml = newPageHtml.lower()

    loginStrs = ["signup", "sign up", "login", "log in", "signin", "sign in"]
    for login in loginStrs:
        if login in pageHtml and login not in newPageHtml:
            vulnReason += f" -- {login} changed"
            break

    #if newPageHtml != pageHtml and (url not in vulnList):
    #    vulnList.append(url)

    titleAfterInjection = driver.title

    # if the title changed, the website is vulnerable
    if titleBeforeInjection != titleAfterInjection:
        vulnReason += f" -- Title changed (redirect)"

    if vulnReason != "":
        print(f"{url} -- VULNERABLE")
        if f'{url}{vulnReason}' not in vulnList:
            vulnList.append(f"{url}{vulnReason}")
    else:
        print(f"{url} -- POSSIBLY SAFE")


    if automatic == False:
        #wait for input before closing
        input("Press enter to close browser\n")

    driver.close()
    driver.quit()
    return

# returns a list of vulnerable websites
def InjectAllAutomatic(short:bool=True, file:str=None) -> 'list[str]':
    domains = []
    sites = []
    if file == None:
        sites = []
        if short:
            sites = getCookies.GetSiteList()
    else:
        with open(file, 'r') as f:
            line = f.readline()
            while line:
                site = line.strip()
                sites.append(site)
                line = f.readline()

    domains = getCookies.GetDomainList(sites)

    vulnList = []
    threads = []

    maxThreads = 8
    idx = 0
    for domain in domains:

        if len(threads) == maxThreads:
            for t in threads:
                t.join()
            threads = []

        print(f"Testing {idx} of {len(domains)}")
        t = threading.Thread(target=lambda: InjectCookiesToDomain(domain, automatic=True, vulnList=vulnList))
        idx += 1
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    return vulnList

if __name__ == '__main__':
    vuln = []
    if len(sys.argv) < 2:
        site = input("Domain you want to visit as <example.com>\n>")
        InjectCookiesToDomain(site, vulnList=vuln)
    else:
        if sys.argv[1] == 'all':
            vuln = InjectAllAutomatic(short = False)
            print(f"Vulnerable: {vuln}")
        elif sys.argv[1] == 'some':
            vuln = InjectAllAutomatic(short = True)
            print(f"Vulnerable: {vuln}")
        elif sys.argv[1] == 'file':
            assert len(sys.argv) >= 3
            vuln = InjectAllAutomatic(file=sys.argv[2])
        else:
            InjectCookiesToDomain(sys.argv[1], vulnList=vuln)
    print("Vulnerable Sites: \n" + '\n'.join(vuln))

