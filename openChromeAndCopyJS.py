import subprocess
import sys
import os
import time
import threading
from selenium import webdriver  # pip install Selenium
from selenium.common.exceptions import WebDriverException
import getCookies

# returns True the title changed after injection
def InjectCookiesToDomain(domain:str, automatic:bool=False, vulnList:'list[str]' = []):
    # URL to open in new window, assume https and .com
    cookies = getCookies.GetCookies(domain)

    if domain[0] != ".":
        domain = "." + domain

    url = f"https://www{domain}"

    # only test the website if we have at least 3 cookies
    if len(cookies) > 3:
        print(f"Testing URL: {url}")
        javascriptCode = \
        f"""
        cookieStr = '{cookies}';
        cookieArr = JSON.parse(cookieStr);
        cookieArr.forEach((item) => {{
            document.cookie = item;
        }})
        """

        driver = webdriver.Chrome()
        driver.set_window_position(100,-1000)
        driver.implicitly_wait(1)

        try:
            driver.get(url)
        except WebDriverException:
            print("Failed to connect on URL: " + url)
            driver.quit()
            return



        titleBeforeInjection = driver.title

        if (automatic == False):
            #wait for input to inject cookies
            input("Press enter to inject cookies\n")

        try:
            driver.execute_script(javascriptCode)
            driver.refresh()
        except WebDriverException:
            print("Exception when executing script: " + url)
            print(f"Script: \n{javascriptCode}")
            driver.quit()
            return

        titleAfterInjection = driver.title

        # if the title changed, the website is vulnerable
        if titleBeforeInjection != titleAfterInjection:
            print(f"{url} -- potentially vulnerable")
            vulnList.append(url)
        else:
            print(f"{url} -- probably safe")

        if automatic == False:
            #wait for input before closing
            input("Press enter to close browser\n")

        driver.quit()
    else:
        print(f"Less than 3 cookies for: {url}")

    return

# returns tuple two lists, (vulnerable, notVulnerable)
def InjectAllAutomatic(short:bool=True) -> 'list[str]':
    domains = getCookies.GetDomainList(short=short)

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
    if len(sys.argv) != 2:
        print("PLEASE PROVIDE THE DOMAIN YOU WANT TO VISIT")
    else:
        if sys.argv[1] == 'all':
            vuln, notVuln = InjectAllAutomatic(short = False)
            print(f"Vulnerable: {vuln}")
        elif sys.argv[1] == 'some':
            vuln = InjectAllAutomatic(short = True)
            print(f"Vulnerable: {vuln}")
        else:
            InjectCookiesToDomain(sys.argv[1])

