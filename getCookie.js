// words and code goes here
console.log("This is a popup!");
chrome.cookies.get({ url: 'https://piazza.com', name: 'piazza_session' },
  function (cookie) {
    if (cookie) {
      console.log(cookie.value);
    } else {
      console.log('Can\'t get cookie!');
    }
});