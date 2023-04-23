# Cookie Collector

The Cookie Collector is a cybersecurity project aimed at demonstrating the risks associated with cookie theft and unauthorized access to user accounts. It involves collecting cookies from Google Chrome and using them to authenticate with a website, without the user's consent. 

### Usage
1. Run `python getcookies.py` to get the Google Chrome cookies 
2. Run the python command `python openChromeAndCopyJS.py` + `domain name` on a command prompt
3. A new Chrome browser will open
4. Press `enter` to inject the cookies into the browser
5. Press `enter` again to close the browser


### `decryptchromecookies.py`

This script is responsible for decrypting the cookies from Google Chrome's cookie database file. It uses the cryptography library to decrypt the encrypted cookie values stored in the `cookies` table of the `Cookies` database file. The decrypted values are then returned in a dictionary format containing the cookie name, value, and other information.

### `testcookie.js`

This script is a JavaScript code that can be executed in the browser console of Google Chrome. It is used to test if the cookies collected by the `decryptchromecookies.py` script are valid and can be used for authentication. The script reads the cookie values from the browser's cookie store and compares them with the values of the cookies collected by the `decryptchromecookies.py` script. If the cookies match, the user is authenticated, and a success message is displayed in the console. If the cookies do not match, the user is not authenticated, and an error message is displayed in the console.

###`openChromeAndCopyJS.py`

This Python script uses the selenium package to automate the process of collecting cookies from a website. The script launches an instance of the Google Chrome web browser and navigates to the desired website. It then executes a JavaScript file that retrieves the cookies from the current session in the Chrome web browser and returns them as a list of dictionaries. The script iterates through the cookie data and prints the name and value of each cookie. Finally, the script closes the Chrome web browser and exits.
