import subprocess
import sys
import os
import time
from selenium import webdriver  # pip install Selenium
import pyperclip                # pip install Pyperclip
import getCookies

def main(domain:str):
    # URL to open in new window, assume https and .com
    url = f"https://{domain}.com"

    cookies = getCookies.GetCookies(domain)

    if len(cookies) > 0:
        javascriptCode = \
        f"""
        cookieStr = '{cookies}';
        cookieArr = JSON.parse(cookieStr);
        cookieArr.forEach((item) => {{
            document.cookie = item;
        }})
        """

        pyperclip.copy(javascriptCode)

        driver = webdriver.Chrome()
        driver.set_window_position(100,-1000)
        driver.get(url)
        driver.implicitly_wait(2)
        #wait for input to inject cookies
        input("Press enter to inject cookies\n")

        driver.execute_script(javascriptCode)
        driver.implicitly_wait(2)
        driver.refresh()

        #wait for input before closing
        input("Press enter to close browser\n")
    else:
        print("No cookies for domain: " + domain)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("PLEASE PROVIDE THE DOMAIN YOU WANT TO VISIT")
    else:
        main(sys.argv[1])
