# Cookie Collector

The Cookie Collector is a cybersecurity project aimed at demonstrating the risks associated with cookie theft and unauthorized access to user accounts. It involves collecting cookies from Google Chrome and using them to authenticate with a website, without the user's consent. 




### `decryptchromecookies.py`

This script is responsible for decrypting the cookies from Google Chrome's cookie database file. It uses the cryptography library to decrypt the encrypted cookie values stored in the `cookies` table of the `Cookies` database file. The decrypted values are then returned in a dictionary format containing the cookie name, value, and other information.

### `testcookie.js`

This script is a JavaScript code that can be executed in the browser console of Google Chrome. It is used to test if the cookies collected by the `decryptchromecookies.py` script are valid and can be used for authentication. The script reads the cookie values from the browser's cookie store and compares them with the values of the cookies collected by the `decryptchromecookies.py` script. If the cookies match, the user is authenticated, and a success message is displayed in the console. If the cookies do not match, the user is not authenticated, and an error message is displayed in the console.

