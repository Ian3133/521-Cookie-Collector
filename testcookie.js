const https = require('https');

function sendCookies(domain) {
    let cookies = [];
    for (let i=1; i<arguments.length; i++) {
        cookies.push(arguments[i]);
    }

    let options = {
        host: domain,
        method: 'GET',
        path: '/',
        headers: {'Cookie': cookies}
    };

    let req = https.request(options, function(res) {
        console.log('Status: ' + res.statusCode);
        console.log('Headers: ' + JSON.stringify(res.headers));
        res.setEncoding('utf8');
        res.on('data', function (chunk) {
            console.log('Body: ' + chunk);
        });
    });

    req.on('error', function(e) {
        console.log('Problem with request: ' + e.message);
    });

    req.end();
}

sendCookies('localhost', 'cookieName=123');
