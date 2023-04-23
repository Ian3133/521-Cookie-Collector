# Cookie Collector

The Cookie Collector is a cybersecurity project aimed at demonstrating the risks associated with cookie theft and unauthorized access to user accounts. It involves collecting cookies from Google Chrome and using them to authenticate with a website, without the user's consent. This project is for educational purposes only and should not be used for any malicious activities.


## Usage
## Usage

1. Launch Google Chrome and navigate to the website from which you want to steal cookies.
2. Click on the `The Cookie Collector` icon in the extensions bar to launch the extension.
3. Click on the `Collect Cookies` button to collect the cookies from the current tab.
4. The cookies will be displayed in the console.
5. Copy the cookies and use them to authenticate with the website using the browser's console or other tools.

It is important to note that cookie theft and unauthorized access to user accounts are highly unethical and illegal activities. The 521 Cookie Collector project is intended for educational purposes only and should not be used for any malicious activities. 




### `decryptchromecookies.py`

This script is responsible for decrypting the cookies from Google Chrome's cookie database file. It uses the cryptography library to decrypt the encrypted cookie values stored in the `cookies` table of the `Cookies` database file. The decrypted values are then returned in a dictionary format containing the cookie name, value, and other information.

### `testcookie.js`

This script is a JavaScript code that can be executed in the browser console of Google Chrome. It is used to test if the cookies collected by the `decryptchromecookies.py` script are valid and can be used for authentication. The script reads the cookie values from the browser's cookie store and compares them with the values of the cookies collected by the `decryptchromecookies.py` script. If the cookies match, the user is authenticated, and a success message is displayed in the console. If the cookies do not match, the user is not authenticated, and an error message is displayed in the console.

Both these scripts are critical components of your project, as they allow the user to collect and authenticate with the stolen cookies. However, it is important to emphasize that such activities are highly unethical and illegal, and the project is intended for educational purposes only.
